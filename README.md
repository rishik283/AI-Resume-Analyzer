# AI Resume Analyzer

AI Resume Analyzer is a simple Streamlit application that uploads a PDF resume, extracts the text, and detects technical skills from a predefined skill list.

## Features
- Upload resumes in PDF format
- Extract text from the uploaded PDF
- Detect technical skills from the resume
- Show matched skills, confidence levels, and a best-match job role suggestion
- Download a text report of the analysis

## Setup
1. Create a Python virtual environment (optional but recommended)
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```

## GitHub Upload
1. Create a new repository on GitHub.
2. Run:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
   git branch -M main
   git push -u origin main
   ```

## Deploy to Streamlit Cloud
1. Push the project to GitHub.
2. Open Streamlit Cloud.
3. Click New app.
4. Select the GitHub repository and the main branch.
5. Set the app file path to app.py.
6. Deploy.

## Project Structure
```text
resume_analyzer/
├── app.py
├── requirements.txt
├── resumes/
└── README.md
```
