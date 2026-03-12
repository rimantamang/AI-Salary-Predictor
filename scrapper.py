import requests
from bs4 import BeautifulSoup
import json

jobs = []

url = "https://realpython.github.io/fake-jobs/"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

job_cards = soup.find_all("div", class_="card-content")

for job in job_cards:
    title = job.find("h2", class_="title").text.strip()
    company = job.find("h3", class_="company").text.strip()
    location = job.find("p", class_="location").text.strip()
    description = job.find("div", class_="content").text.strip()

    job_data = {
        "title": title,
        "company": company,
        "location": location,
        "description": description,
        "salary": None
    }

    jobs.append(job_data)

with open("jobs_raw.json", "w") as f:
    json.dump(jobs, f, indent=4)

print("Data saved to jobs_raw.json")
