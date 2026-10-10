# AI ATS Resume Analyzer

An AI-powered Applicant Tracking System (ATS) that analyzes resumes against job descriptions, evaluates candidate suitability, identifies skill gaps, and generates actionable feedback to improve resume quality.

## Overview

AI ATS Resume Analyzer is a Python-based application designed to streamline resume screening and candidate evaluation. It combines natural language processing, retrieval-based techniques, and AI-powered analysis to help users understand how well a resume matches a job description.

## Features

* **Resume Analysis:** Extract and analyze information from uploaded resumes.
* **Job Description Analysis:** Identify key skills, qualifications, and requirements from job descriptions.
* **Resume Matching:** Evaluate the alignment between candidate profiles and job requirements.
* **Skill Gap Analysis:** Highlight missing or underrepresented skills.
* **Resume Quality Assessment:** Analyze resume quality and suggest improvements.
* **AI-Generated Feedback:** Provide personalized recommendations for improving resumes.
* **Interview Preparation:** Generate interview questions based on relevant candidate and job information.
* **Recruiter Dashboard:** Present candidate evaluation results and comparisons.
* **PDF Processing:** Support resume text extraction and report generation.

## Technology Stack

* **Language:** Python
* **Interface:** Streamlit
* **AI and LLM Integration:** Configured language-model integrations
* **NLP and Retrieval:** Resume parsing, text processing, embeddings, and retrieval components
* **Data Management:** Database integration
* **Testing:** pytest-compatible test suite

## Project Structure

```text
AI-ATS-RESUME-ANALYZER/
├── agents/              # AI analysis and evaluation agents
├── components/          # Reusable interface components
├── database/            # Database operations
├── pages/               # Dashboard pages
├── prompts/             # LLM prompt templates
├── services/            # Application services
├── static/              # CSS and static assets
├── tests/               # Automated tests
├── utils/               # PDF, retrieval, and scoring utilities
├── app.py               # Main application module
├── streamlit_app.py     # Streamlit application entry point
├── config.py            # Application configuration
├── graph.py             # Agent workflow graph
├── rag.py               # Retrieval-augmented generation logic
├── requirements.txt     # Python dependencies
├── resume_parser.py     # Resume parsing
├── schemas.py           # Data schemas
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Sohail-ahmad-ux/AI-ATS-RESUME-ANALYZER.git
cd AI-ATS-RESUME-ANALYZER
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Review `config.py` to identify the API keys and configuration required by your application.

Store credentials in a local `.env` file or environment variables, according to the configuration your code expects. Never commit API keys, passwords, private resumes, or other sensitive information to GitHub.

### 5. Run the application

Try the Streamlit entry point:

```bash
streamlit run streamlit_app.py
```

If your project uses `app.py` as the actual entry point, run:

```bash
streamlit run app.py
```

Use the entry point configured for your application.

## Testing

Run the automated tests with:

```bash
python -m pytest tests/
```

Some tests may require API credentials, additional configuration, or test data. Configure these dependencies before running them.

## Use Cases

* Resume-to-job-description matching
* Candidate skill and qualification analysis
* Resume quality improvement
* Interview preparation
* Candidate comparison and recruiter support

## Limitations

This project is intended to assist resume review and candidate evaluation. Its scores and AI-generated recommendations should not be treated as definitive hiring decisions. Results may vary depending on resume quality, job-description clarity, model behavior, and configuration.

## Future Improvements

* Benchmark resume-matching performance against a labeled dataset
* Add explainable scoring and evidence for individual recommendations
* Evaluate extraction accuracy and matching quality
* Improve fairness and consistency across candidate profiles
* Deploy the application with secure configuration and controlled access

## Author

**Sohail Ahmad**

Aspiring AI/ML Engineer | NLP | Generative AI | Agentic AI

* GitHub: [Sohail-ahmad-ux](https://github.com/Sohail-ahmad-ux)
* Project Repository: [AI ATS Resume Analyzer](https://github.com/Sohail-ahmad-ux/AI-ATS-RESUME-ANALYZER)

## License

Add a license file to specify the terms under which others may use, modify, and distribute this project.
