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

Input Sources
   ↓
Text Extraction
   ├── Resume Parsing (LLM + Experience Calculation)
   └── Resume Chunking → Resume Embeddings
       + Job Description → JD Embedding
             ↓
       Cosine Similarity
             ↓
       Top-K Matching
             ↓
       Score Aggregation
             ↓
       Candidate Ranking
             ↓
       Streamlit UI
             ↓
       Excel Export
