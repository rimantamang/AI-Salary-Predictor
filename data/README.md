# AI-Salary-Predictor

📊 Job Data Processing Pipeline
🧠 Overview

This project is a data processing pipeline designed to transform raw job listings (in JSON format) into clean, structured datasets (CSV files). The pipeline extracts meaningful features such as experience, salary, remote work availability, and job-specific skills, and organizes the data into multiple category-based datasets.

⚙️ What This Code Does

The script performs the following major tasks:

1. 📂 Load Raw Data
Reads a JSON file containing job listings.
Each job entry typically includes:
Job title
Company name
Job description
2. 🧠 Category Detection

Each job is classified into one of four categories based on keywords:

Tech
Medical
Finance
Other

This is done by analyzing both:

Job title
Job description
3. 🔍 Feature Extraction

The pipeline extracts important features from job descriptions:

✅ Experience
Extracts years of experience using regex patterns.
Handles formats like:
"3+ years"
"2-4 years"
"5 years"
Falls back to keywords:
Senior → 5 years
Mid → 3 years
Junior/Entry → 1 year
💰 Salary
Extracts salary values only when relevant keywords are present.
Supports formats like:
"50000-70000"
"60000"
"50k"
Avoids incorrect extraction (e.g., phone numbers).
🌍 Remote Work
Detects if a job is remote-friendly based on keywords like:
"remote"
"work from home"
"wfh"
4. 🧩 Category-Specific Features

Additional features are extracted depending on job category:

💻 Tech Jobs
Python skill
Django skill
AWS knowledge
🏥 Medical Jobs
Medical license requirement
Patient care involvement
Clinical experience
💼 Finance Jobs
Financial analysis
Risk management
Accounting
5. 🧹 Data Cleaning
Removes unnecessary whitespace
Ensures consistent data types
Keeps missing values as None instead of inserting fake data
Standardizes fields like:
job_title
company
salary_min
experience_years
6. 📊 Data Organization

Jobs are separated into four datasets:

tech_jobs
medical_jobs
finance_jobs
other_jobs

Each dataset contains:

Base features (title, company, salary, etc.)
Category-specific features
7. 💾 Output Generation

The processed data is saved as CSV files:

/data/
│
├── tech_jobs.csv
├── medical_jobs.csv
├── finance_jobs.csv
└── other_jobs.csv

Each CSV:

Contains structured, clean data
Has duplicates removed
Is ready for analysis or machine learning
🔁 How the Pipeline Works (Step-by-Step)
Load JSON file
Loop through each job entry
Extract description and title
Detect job category
Extract:
Experience
Salary
Remote status
Clean the extracted data
Add category-specific features
Store in corresponding list
Convert lists into DataFrames
Save as CSV files
🚀 How to Run
Make sure your JSON file is located at:
../scraper/jobs_raws.json
Run the script:
python your_script_name.py
Output CSV files will be created in:
../data/
📈 Use Cases

This dataset can be used for:

Salary prediction models
Job classification tasks
Data analysis and visualization
Machine learning projects
💡 Key Highlights
Modular and scalable design
Robust text processing using regex
Clean and ML-ready datasets
Efficient and easy to extend
🔮 Future Improvements
Add more job categories
Improve NLP-based classification
Integrate machine learning models
Add visualization dashboards
🏁 Conclusion

This project demonstrates a complete pipeline for transforming unstructured job data into structured datasets. It serves as a strong foundation for further data analysis and AI model development.