# Intelligent-Resume-Screening-System

A resume screening system that analyzes resumes against a job description, ranks candidates based on relevance, and generates structured reports.

## Overview

The Intelligent Resume Screening System is a backend application that processes resumes and ranks candidates based on their relevance to a given job description.

The system extracts structured information from resumes, calculates total experience, and evaluates candidate suitability using semantic similarity. It also provides a user interface for uploading resumes and generating structured reports.

---

## Features

- Resume parsing from PDF files
- Extraction of candidate details (name, skills, education, summary)
- Experience calculation from date ranges
- Resume segmentation into smaller sections
- Similarity-based matching with job descriptions
- Candidate scoring and ranking
- Excel report generation for candidates
- Web interface built using Streamlit
- Robust error handling

---

## Workflow

1. Load resume PDF and extract text  
2. Extract structured information from resume  
3. Calculate total work experience  
4. Split resume into smaller sections  
5. Convert text into numerical representations  
6. Compare with job description  
7. Generate similarity score  
8. Rank candidates  
9. Export results as Excel report  

---
## System Flow

```
┌──────────────────────────────────────────────────────────────┐
│       INTELLIGENT RESUME SCREENING SYSTEM ARCHITECTURE       │
└──────────────────────────────────────────────────────────────┘
                        │
                        ▼
          ┌───────────────────────────┐
          │      INPUT SOURCES        │
          │ (Resume PDFs + Job Desc)  │
          └─────────────┬─────────────┘
                        │
                        ▼
          ┌───────────────────────────┐
          │      TEXT EXTRACTION      │
          └─────────────┬─────────────┘

     ┌──────────────────┼──────────────────┐
     ▼                  ▼                  ▼

┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ RESUME       │  │ JOB          │  │ RESUME       │
│ CHUNKING     │  │ DESCRIPTION  │  │ PARSING      │
│ (split text) │  │ (raw text)   │  │ (LLM extract)│
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       ▼                  ▼                 ▼

┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ RESUME       │  │ JD           │  │ EXPERIENCE   │
│ EMBEDDINGS   │  │ EMBEDDING    │  │ CALCULATION  │
│ (MiniLM)     │  │ (MiniLM)     │  │ (dates)      │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                  │                 │
       └──────────┬───────┴──────────┬──────┘
                  ▼                  ▼

        ┌──────────────────────────────┐
        │   COSINE SIMILARITY ENGINE   │
        │ (semantic matching + top-k)  │
        └──────────────┬───────────────┘
                       │
                       ▼

        ┌──────────────────────────────┐
        │     CANDIDATE RANKING        │
        │ (score aggregation)          │
        └──────────────┬───────────────┘
                       │
                       ▼

        ┌──────────────────────────────┐
        │   STREAMLIT WEB INTERFACE    │
        └──────────────┬───────────────┘
                       │
                       ▼

        ┌──────────────────────────────┐
        │     EXCEL REPORT EXPORT      │
        └──────────────────────────────┘
```
---

## How it Works

-	Resumes are split into smaller chunks to capture detailed context
-	Each chunk is converted into a vector using a transformer-based embedding model
- The job description is converted into a single embedding
-	Cosine similarity is computed between the job description and each resume chunk
-	The top matching sections are selected and averaged to generate a final score
-	Candidates are ranked based on this score


---

## Tech Stack

- Python
- LangChain
- HuggingFace Embeddings
- Sentence Transformers (all-MiniLM-L6-v2)
- NumPy
- Scikit-learn
- Streamlit
- OpenPyXL
- Regex

---

## Similarity Method

- Resume is divided into smaller sections (chunks)
- Each section is converted into embeddings
- Job description is also converted into embeddings
- Cosine similarity is computed between job description and each section
- Top matching sections are selected
- Final score is calculated as the average of top matches

---

## Running the Project
1. Clone the Repository
```
git clone https://github.com/your-username/Intelligent-Resume-Screening-System.git
cd Intelligent-Resume-Screening-System
```

3. Install Dependencies
```
pip install -r requirements.txt
```

5. Configure Environment
Create a .env file in the root directory and add:
```
HF_TOKEN=your_huggingface_token
```
5. Run the Application
```
streamlit run app.py
```

---
## Output

After running the system, the application provides:

- Ranked list of candidates based on relevance to the job description 
- Match score (percentage) for each candidate 
- Extracted skills from resumes 
-	Work experience calculated from date ranges 
- Education details 
- Generated professional summary 
- Downloadable Excel report directly from the Streamlit interface 

---
## Future Improvements

- Integration of an HR chatbot for interacting with candidate insights 
- Candidate-side chatbot to evaluate and match skills with job descriptions 
- Fully automated recruitment workflow for HR teams 
-	Support for additional file formats such as DOCX and TXT 
- Advanced filtering, sorting, and search features in the UI 


---
## License

Released under the MIT License, enabling open use, modification, and distribution with attribution.
