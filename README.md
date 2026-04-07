# Intelligent-Resume-Screening-System

A resume screening system with automated candidate ranking and reporting.

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
System Flow

================================================================================
                    INTELLIGENT RESUME SCREENING SYSTEM ARCHITECTURE
================================================================================
       |
       ▼
+---------------+
| Input Sources | (Resume PDFs, Job Desc.)
+---------------+
       |
       ▼
+---------------+
| Text Extraction| (PDF to text, raw JD)
+---------------+
       |
       ▼
       +-------------------------------+------------------------------+
       |                               |                              |
       ▼                               ▼                              ▼
[ RESUME CHUNKING ]         [ Job Description ]          [ RESUME PARSING ]
   (Split text)               (NO chunking)               (Extract Name, Skills,
   |                             |                        Summary via LLM)
   ▼                             |                              |
[ Embedding Model ]         [ Embedding Model ]                |
   (Sentence-Transformers       (Sentence-Transformers         [ Experience Calc ]
    MiniLM vectors)              MiniLM vectors)               (Date parsing)
   |                             |                              |
   |                             |                              |
   ▼                             ▼                              |
   +--------------+----------------+                              |
                  |                                              |
                  ▼                                              |
        (VECTOR SPACE SEMANTIC MATCHING)                         |
                  |                                              |
                  ▼                                              |
      [ COSINE SIMILARITY ENGINE ]                               |
      (HuggingFace Embeddings)                                   |
                  |                                              |
                  ▼                                              |
          [ TOP-K MATCHING ]                                     |
          (Aggregate similarity scores)                          |
                  |                                              |
                  ▼                                              |
          [ CANDIDATE RANKING ] <--------------------------------+
          (Rank by aggreg. scores AND parsed data)
                  |
                  ▼
          [ STREAMLIT WEB APPLICATION ]
          (Upload, Display, Score Bars, skills, etc.)
                  |
                  ▼
          [ EXCEL REPORT EXPORT ]
          (Downloadable .xlsx report)
================================================================================
