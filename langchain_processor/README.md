#  AI-Powered Feature Extraction Pipeline

##  My Role
My responsibility in this project was to design and implement the **LLM Extraction Layer**. This involves taking raw, unstructured job data (JSON) and transforming it into a structured format (CSV) that can be used to train our Salary Prediction machine learning models.

## ⚙️ How the Pipeline Works

### 1. Data Orchestration
I used **LangChain** to create a structured processing chain. This connects our raw input text to the **Llama-3.1-8B** model (hosted on **Groq**) to perform high-speed natural language analysis.

### 2. Schema Enforcement & Validation
To ensure the data is "clean" for the Data Science team, I implemented **Pydantic** models. This forces the AI to extract exactly what we need in a strict format:
*   **Categories**: Maps jobs into specific sectors (Tech, Medical, Finance, etc.).
*   **Numerical Features**: Extracts years of experience and minimum salary as integers.
*   **Skill Binary Flags**: Identifies the presence of 5 core skill sets:
    *   `IT_skill` (Coding/Data)
    *   `Medical_skill` (Clinical/Healthcare)
    *   `Financial_skill` (Accounting/Banking)
    *   `Business_skill` (Management/Sales)
    *   `Technical_skill` (Engineering/Trades like Plumbing & Electrical)

### 3. Error Handling & Persistence
The script is designed for reliability:
*   **Persistence**: Uses a `try-finally` block to ensure that if the script crashes or is stopped, all data processed up to that point is saved to `jobs_dataset.csv`.
*   **Rate Limiting**: Includes automated time delays to respect Groq's API limits.
*   **Context Management**: Automatically truncates long job descriptions to optimize token usage and cost.

##  How to Run
1. Navigate to the `langchain_processor` folder.
2. Ensure your `.env` file contains your `GROQ_API_KEY`.
3. Run the script:
   ```bash
   python extract_features.py
   ```
4. The output will be generated at `../data/jobs_dataset.csv`.