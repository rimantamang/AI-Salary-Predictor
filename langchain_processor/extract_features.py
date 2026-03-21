import os
import json
import time
import re
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# =========================
# 1. Setup
# =========================
load_dotenv()

class JobFeatures(BaseModel):
    experience_years: int = Field(description="Minimum years of experience (integer)")
    python_skill: int = Field(description="1 if Python is mentioned, else 0")
    django_skill: int = Field(description="1 if Django is mentioned, else 0")
    aws_skill: int = Field(description="1 if AWS is mentioned, else 0")
    remote_friendly: int = Field(description="1 if remote/hybrid, else 0")
    salary_min_k: int = Field(description="Minimum salary in thousands (integer)")

# =========================
# 2. Initialize TinyLlama
# =========================
llm = HuggingFaceEndpoint(
    repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    task="text-generation",
    max_new_tokens=256,
    temperature=0.1,
    huggingfacehub_api_token=os.getenv("HUGGING_FACE_API_KEY")
)

chat_model = ChatHuggingFace(llm=llm)
parser = JsonOutputParser(pydantic_object=JobFeatures)

# =========================
# 3. Prompt (STRONG)
# =========================
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You MUST return ONLY valid JSON.\n"
     "{format_instructions}\n\n"
     "Rules:\n"
     "- If experience not found → 0\n"
     "- If skill not mentioned → 0\n"
     "- Detect Python, Django, AWS\n"
     "- Remote includes: remote, hybrid, work from home\n"
     "- Output ONLY JSON"
    ),
    ("human", "Job description:\n{description}")
])

chain = prompt | chat_model | parser

# =========================
# 4. Fallback Extraction
# =========================
def fallback_extract(desc):
    desc_lower = desc.lower()

    return {
        "experience_years": 0,
        "python_skill": int("python" in desc_lower),
        "django_skill": int("django" in desc_lower),
        "aws_skill": int("aws" in desc_lower),
        "remote_friendly": int(
            any(word in desc_lower for word in ["remote", "hybrid", "work from home"])
        ),
        "salary_min_k": extract_salary(desc)
    }

# =========================
# 5. Salary Extraction (Regex)
# =========================
def extract_salary(desc):
    desc = desc.lower()

    # Match formats like 80k, 100k
    match = re.search(r'(\d{2,3})\s?k', desc)
    if match:
        return int(match.group(1))

    return 0

# =========================
# 6. Data Cleaning
# =========================
def clean_features(f):
    return {
        "experience_years": max(0, int(f.get("experience_years", 0))),
        "python_skill": int(f.get("python_skill", 0)),
        "django_skill": int(f.get("django_skill", 0)),
        "aws_skill": int(f.get("aws_skill", 0)),
        "remote_friendly": int(f.get("remote_friendly", 0)),
        "salary_min_k": max(0, int(f.get("salary_min_k", 0))),
    }

# =========================
# 7. Main Processing
# =========================
def process_all_jobs():
    input_file = "../scraper/jobs_raws.json"
    output_file = "../data/jobs_dataset.csv"

    if not os.path.exists(input_file):
        print(f"❌ Error: {input_file} not found.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        raw_jobs = json.load(f)

    processed_data = []

    print(f"🚀 Processing {len(raw_jobs)} jobs...")

    for job in tqdm(raw_jobs, desc="Extracting"):
        desc = job.get("description", "")

        if not desc:
            continue

        try:
            # LLM extraction
            features = chain.invoke({
                "description": desc[:1000],
                "format_instructions": parser.get_format_instructions()
            })

        except Exception:
            # Fallback if LLM fails
            features = fallback_extract(desc)

            # Log failure
            with open("failed_jobs.log", "a", encoding="utf-8") as log:
                log.write(desc[:300] + "\n\n")

        # Clean data
        features = clean_features(features)

        # Override salary with regex (more reliable)
        features["salary_min_k"] = extract_salary(desc)

        processed_data.append({
            "job_title": job.get("job_title"),
            "company": job.get("company"),
            **features
        })

        time.sleep(0.3)

    # =========================
    # Save Output
    # =========================
    if processed_data:
        df = pd.DataFrame(processed_data)

        os.makedirs("../data", exist_ok=True)
        df.to_csv(output_file, index=False)

        print(f"\n✅ Done! {len(processed_data)} jobs saved to {output_file}")
    else:
        print("\n❌ No data processed.")

# =========================
# 8. Run Script
# =========================
if __name__ == "__main__":
    process_all_jobs()