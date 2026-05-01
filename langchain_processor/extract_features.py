import os
import json
import time
import pandas as pd
from tqdm import tqdm
from typing import List
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field 
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

# --- 1. SETUP ---
load_dotenv() 
groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model_name="llama-3.1-8b-instant",
    temperature=0,
    groq_api_key=groq_api_key
)

# --- 2. THE SCHEMA (Updated: Batching enabled, technical_skill removed) ---
class JobFeatures(BaseModel):
    category: str = Field(description="One of: tech, medical, finance, other")
    experience_years: int = Field(description="Numeric years of experience. Default to 0.")
    salary_min: int = Field(description="Lower bound annual salary. Default to 0.")
    remote_friendly: int = Field(description="1 if remote/WFH/hybrid, 0 if office")
    it_skill: int = Field(description="1 if coding/software/data/IT, else 0")
    medical_skill: int = Field(description="1 if healthcare/nursing/clinical, else 0")
    financial_skill: int = Field(description="1 if accounting/banking/finance, else 0")
    business_skill: int = Field(description="1 if management/sales/marketing/ops, else 0")

class JobBatch(BaseModel):
    jobs: List[JobFeatures]

parser = PydanticOutputParser(pydantic_object=JobBatch)

prompt = PromptTemplate(
    template="Analyze these {count} jobs and extract features for EACH. Respond ONLY with valid JSON.\n{format_instructions}\nJobs:\n{jobs_text}",
    input_variables=["jobs_text", "count"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | llm | parser

# --- 3. THE PIPELINE ---
def process_to_master_csv():
    input_file = "../scraper/jobs_raws.json" 
    output_file = "../data/jobs_dataset.csv"
    batch_size = 5 

    if not os.path.exists(input_file): return

    with open(input_file, 'r', encoding='utf-8') as f:
        jobs = json.load(f)

    processed_data = []
    print(f"🚀 Starting BATCH extraction (Size: {batch_size}) for {len(jobs)} jobs...")

    try:
        # Step through the list in chunks of 5
        for i in tqdm(range(0, len(jobs), batch_size)): 
            chunk = jobs[i:i + batch_size]
            try:
                jobs_text = ""
                for idx, j in enumerate(chunk):
                    # Aggressive truncation (800 chars) for speed
                    jobs_text += f"--- JOB {idx} ---\nTitle: {j.get('job_title')}\nDesc: {j.get('description', '')[:800]}\n\n"
                
                response = chain.invoke({"jobs_text": jobs_text, "count": len(chunk)})
                
                for idx, features in enumerate(response.jobs):
                    # Using model_dump() to avoid the Pydantic warning
                    record = {
                        "job_title": chunk[idx].get("job_title"),
                        "company": chunk[idx].get("company"),
                        **features.model_dump()
                    }
                    processed_data.append(record)
                
                time.sleep(1.5) 

            except Exception as e:
                # If a batch fails, we don't want to stop the whole script
                print(f"Error in batch starting at index {i}: {e}")
                continue
    finally:
        if processed_data:
            os.makedirs("../data", exist_ok=True)
            df = pd.DataFrame(processed_data)
            df.to_csv(output_file, index=False)
            print(f"\n✅ SUCCESS! {len(df)} records saved to {output_file}")

if __name__ == "__main__":
    process_to_master_csv()
