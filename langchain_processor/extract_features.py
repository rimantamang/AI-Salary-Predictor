import os
import json
import re
import pandas as pd
from tqdm import tqdm

# =========================
# 1. CATEGORY DETECTION
# =========================
def detect_category(title, desc):
    text = (title + " " + desc).lower()

    # prioritize skills over generic titles
    if any(k in text for k in ["python", "developer", "software", "backend", "frontend", "aws"]):
        return "tech"
    elif any(k in text for k in ["nurse", "doctor", "clinical", "medical", "health"]):
        return "medical"
    elif any(k in text for k in ["finance", "analyst", "account", "bank", "financial"]):
        return "finance"
    else:
        return "other"

# =========================
# 2. EXPERIENCE EXTRACTION
# =========================
def extract_experience(desc):
    desc = desc.lower()

    # match "3-5 years" or "2 to 4 years"
    match = re.search(r'(\d+)\s?[-to]+\s?(\d+)\s*(years|yrs)', desc)
    if match:
        return int(match.group(1))

    # match "3+ years"
    match = re.search(r'(\d+)\+?\s*(years|yrs)', desc)
    if match:
        return int(match.group(1))

    # fallback using keywords
    if "senior" in desc:
        return 5
    if "mid" in desc:
        return 3
    if "junior" in desc or "entry" in desc:
        return 1

    return None

# =========================
# 3. SALARY EXTRACTION
# =========================
def extract_salary(desc):
    desc = desc.lower().replace(",", "")

    # only consider salary-related context
    if not any(k in desc for k in ["salary", "pay", "$", "₹"]):
        return None

    # range: 50000-70000
    match = re.search(r'(\d{5,6})\s?[-to]+\s?(\d{5,6})', desc)
    if match:
        return int(match.group(1))

    # single number
    match = re.search(r'\b(\d{5,6})\b', desc)
    if match:
        return int(match.group(1))

    # 50k format
    match = re.search(r'(\d{2,3})\s?k', desc)
    if match:
        return int(match.group(1)) * 1000

    return None

# =========================
# 4. REMOTE DETECTION
# =========================
def extract_remote(desc):
    keywords = ["remote", "work from home", "wfh", "anywhere"]
    return int(any(k in desc.lower() for k in keywords))

# =========================
# 5. CATEGORY FEATURES
# =========================
def extract_tech(desc):
    desc = desc.lower()
    return {
        "python_skill": int("python" in desc),
        "django_skill": int("django" in desc),
        "aws_skill": int("aws" in desc or "amazon web services" in desc)
    }

def extract_medical(desc):
    desc = desc.lower()
    return {
        "medical_license": int("license" in desc),
        "patient_care": int("patient" in desc),
        "clinical_experience": int("clinical" in desc)
    }

def extract_finance(desc):
    desc = desc.lower()
    return {
        "financial_analysis": int("analysis" in desc),
        "risk_management": int("risk" in desc),
        "accounting": int("account" in desc)
    }

# =========================
# 6. CLEANING
# =========================
def clean_base(data):
    return {
        "job_title": str(data.get("job_title", "")).strip(),
        "company": str(data.get("company", "")).strip(),
        "experience_years": data.get("experience_years"),
        "salary_min": data.get("salary_min"),  # no fake defaults
        "remote_friendly": int(data.get("remote_friendly", 0))
    }

# =========================
# 7. MAIN PIPELINE
# =========================
def process_jobs():
    input_file = "../scraper/jobs_raws.json"

    tech_jobs, medical_jobs, finance_jobs, other_jobs = [], [], [], []

    with open(input_file, 'r', encoding='utf-8') as f:
        jobs = json.load(f)

    print(f" Processing {len(jobs)} jobs...")

    for job in tqdm(jobs):
        desc = job.get("description", "")
        title = job.get("job_title", "")

        if not desc:
            continue

        category = detect_category(title, desc)

        base = {
            "job_title": title,
            "company": job.get("company"),
            "experience_years": extract_experience(desc),
            "salary_min": extract_salary(desc),
            "remote_friendly": extract_remote(desc)
        }

        base = clean_base(base)

        # add category-specific features
        if category == "tech":
            base.update(extract_tech(desc))
            tech_jobs.append(base)

        elif category == "medical":
            base.update(extract_medical(desc))
            medical_jobs.append(base)

        elif category == "finance":
            base.update(extract_finance(desc))
            finance_jobs.append(base)

        else:
            other_jobs.append(base)

    # =========================
    # SAVE FILES
    # =========================
    os.makedirs("../data", exist_ok=True)

    pd.DataFrame(tech_jobs).drop_duplicates().to_csv("../data/tech_jobs.csv", index=False)
    pd.DataFrame(medical_jobs).drop_duplicates().to_csv("../data/medical_jobs.csv", index=False)
    pd.DataFrame(finance_jobs).drop_duplicates().to_csv("../data/finance_jobs.csv", index=False)
    pd.DataFrame(other_jobs).drop_duplicates().to_csv("../data/other_jobs.csv", index=False)

    # =========================
    # LOGGING
    # =========================
    print("\n DONE!")
    print(f"Tech jobs: {len(tech_jobs)}")
    print(f"Medical jobs: {len(medical_jobs)}")
    print(f"Finance jobs: {len(finance_jobs)}")
    print(f"Other jobs: {len(other_jobs)}")

# =========================
# RUN
# =========================
if __name__ == "__main__":
    process_jobs()