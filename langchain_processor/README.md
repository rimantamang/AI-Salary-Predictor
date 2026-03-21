#  Feature Extraction Pipeline (My Contribution)

This part of the project focuses on transforming raw job data into a structured dataset using AI-based processing.

I built a data processing pipeline using LangChain and Hugging Face models to extract meaningful features from unstructured job listings.

---

##  What I Did

- Developed a script to process raw job data (`jobs_raws.json`)
- Used AI models to extract structured information such as:
  - Job title
  - Skills
  - Experience level
  - Salary (if available)
- Designed prompts to guide the model for consistent outputs
- Validated outputs using Pydantic models
- Converted processed data into a clean CSV file (`jobs_dataset.csv`)
- Implemented logging for failed or incomplete extractions

---

##  How It Works

1. Load raw job data from JSON  
2. Send each job entry to the language model  
3. Extract structured fields using prompt + parsing  
4. Validate the response format  
5. Save results into a CSV file  
6. Log errors into `failed_jobs.log`  

---

##  Technologies Used

- Python  
- LangChain  
- Hugging Face API  
- Pandas  
- Pydantic  
- dotenv  
- tqdm  

---

##  Key Files

- `extract_features.py` → Main processing script  
- `.env` → Stores API key  
- `failed_jobs.log` → Tracks failed cases  
- `jobs_dataset.csv` → Final structured dataset  

---

##  Output

The pipeline generates a structured dataset from raw job listings, making it suitable for:

- Machine learning models  
- Salary prediction  
- Data analysis  

---


## Summary

This component automates the conversion of unstructured job data into a clean, structured format using AI, forming a critical step for downstream analysis and modeling.