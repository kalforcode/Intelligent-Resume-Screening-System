from dotenv import load_dotenv
load_dotenv()

import os
import json
import re
import numpy as np
from datetime import datetime
from typing import List, Dict

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from huggingface_hub import InferenceClient

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

HF_TOKEN = os.environ.get("HF_TOKEN", "")
hf_client = InferenceClient(token=HF_TOKEN)

PRESENT = datetime(2026, 4, 1)

MONTH_MAP = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
    "january": 1, "february": 2, "march": 3, "april": 4, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10,
    "november": 11, "december": 12
}

def parse_date(s: str):
    try:
        s = s.strip().lower()
        if any(x in s for x in ["present", "current", "now"]):
            return PRESENT
        m = re.match(r'([a-z]+)\.?\s+(\d{4})', s)
        if m:
            month = MONTH_MAP.get(m.group(1)[:3], 1)
            return datetime(int(m.group(2)), month, 1)
        m = re.match(r'(\d{1,2})[/-](\d{4})', s)
        if m:
            return datetime(int(m.group(2)), int(m.group(1)), 1)
        m = re.match(r'(\d{4})', s)
        if m:
            return datetime(int(m.group(1)), 1, 1)
    except:
        pass
    return None

def calculate_experience(text: str) -> str:
    try:
        lines = text.split('\n')

        WORK_SECTION_KEYWORDS = [
            'professional experience', 'work experience', 'employment history',
            'career history', 'internship experience', 'work history', 'experience'
        ]

        STOP_SECTION_KEYWORDS = [
            'education', 'certifications', 'achievements', 'awards',
            'publications', 'skills', 'volunteer', 'courses', 'projects'
        ]

        work_lines = []
        in_work_section = False

        for line in lines:
            stripped = line.strip()
            line_lower = stripped.lower()

            if any(kw == line_lower or line_lower.startswith(kw) for kw in WORK_SECTION_KEYWORDS):
                in_work_section = True
                continue

            if any(kw == line_lower or line_lower.startswith(kw) for kw in STOP_SECTION_KEYWORDS):
                if in_work_section:
                    in_work_section = False
                continue

            if in_work_section and stripped:
                work_lines.append(stripped)

        work_text = '\n'.join(work_lines)
        print(f"WORK SECTION TEXT:\n{work_text}\n---")

        if not work_text.strip():
            work_text = text

        # Pattern handles regular dash, en-dash (–), em-dash (—), and unicode variants
        date_part = r'([A-Za-z]+\.?\s+\d{4}|\d{1,2}[/-]\d{4}|\d{4})'
        sep = r'\s*[\u2013\u2014\-\–\—]+\s*'
        end_part = r'([A-Za-z]+\.?\s+\d{4}|\d{1,2}[/-]\d{4}|\d{4}|[Pp]resent|[Cc]urrent|[Nn]ow)'
        pattern = date_part + sep + end_part

        matches = re.findall(pattern, work_text)
        print(f"DATE MATCHES: {matches}")

        total_months = 0
        periods = []
        seen = set()

        for start_str, end_str in matches:
            key = (start_str.strip().lower(), end_str.strip().lower())
            if key in seen:
                continue
            seen.add(key)

            start = parse_date(start_str)
            end = parse_date(end_str)
            if start and end and end >= start:
                months = (end.year - start.year) * 12 + (end.month - start.month)
                if 0 < months <= 600:
                    total_months += months
                    periods.append(f"{start_str.strip()} - {end_str.strip()} ({months}m)")

        if total_months == 0:
            return "N/A"

        years = total_months // 12
        months_rem = total_months % 12

        if years > 0 and months_rem > 0:
            duration = f"{years} yr {months_rem} mo"
        elif years > 0:
            duration = f"{years} yr"
        else:
            duration = f"{months_rem} mo"

        return f"{duration} | {', '.join(periods)}"

    except Exception as e:
        print(f"calculate_experience ERROR: {e}")
        return "N/A"


def load_resume(file_path: str) -> str:
    try:
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        text = "\n".join([doc.page_content for doc in docs])
        print(f"PDF LOADED: {len(text)} characters from {len(docs)} pages")
        return text
    except Exception as e:
        print(f"load_resume ERROR: {e}")
        return ""


def parse_resume_hf(text: str) -> Dict:
    prompt = f"""You are an expert HR resume parser.
Read the resume below and return ONLY a valid JSON object with exactly these keys:

{{
  "name": "Full name of the candidate, or Unknown if not found",
  "skills": ["skill1", "skill2", "...all technical and soft skills as array"],
  "education": "Highest qualification and institute name, or N/A",
  "summary": "A concise 3-5 sentence professional summary of the candidate covering their background, key skills, notable achievements, and career focus"
}}

Rules:
- Return ONLY the JSON object
- No markdown, no backticks, no explanation
- skills must be an array of strings
- summary must be a proper paragraph, not bullet points

Resume:
{text[:4000]}"""

    response = hf_client.chat_completion(
        model="meta-llama/Meta-Llama-3-8B-Instruct",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=700,
        temperature=0.01,
    )

    raw = response.choices[0].message.content.strip()
    print(f"HF RAW RESPONSE:\n{raw}")

    raw = re.sub(r'```json|```', '', raw).strip()

    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if match:
        return json.loads(match.group())
    raise ValueError(f"No valid JSON in response: {raw[:200]}")


def parse_resume(text: str) -> Dict:
    fallback = {
        "name": "Unknown",
        "skills": [],
        "experience": "N/A",
        "education": "N/A",
        "summary": "N/A",
    }

    if not text or len(text.strip()) < 50:
        print("Resume text too short or empty")
        fallback["experience"] = calculate_experience(text)
        return fallback

    experience = calculate_experience(text)

    try:
        parsed = parse_resume_hf(text)

        skills = parsed.get("skills", [])
        if isinstance(skills, str):
            try:
                skills = json.loads(skills)
            except:
                skills = [s.strip() for s in skills.split(",") if s.strip()]

        return {
            "name": parsed.get("name", "Unknown") or "Unknown",
            "skills": skills if isinstance(skills, list) else [],
            "experience": experience,
            "education": parsed.get("education", "N/A") or "N/A",
            "summary": parsed.get("summary", "N/A") or "N/A",
        }

    except Exception as e:
        print(f"parse_resume LLM ERROR: {type(e).__name__}: {e}")
        fallback["experience"] = experience
        return fallback


def compute_similarity(jd: str, resume_text: str) -> float:
    try:
        chunks = splitter.split_text(resume_text)
        if not chunks:
            return 0.0

        chunk_embeddings = np.array(embeddings.embed_documents(chunks))
        jd_embedding = np.array(embeddings.embed_query(jd))

        jd_norm = jd_embedding / (np.linalg.norm(jd_embedding) + 1e-10)
        chunk_norms = chunk_embeddings / (
            np.linalg.norm(chunk_embeddings, axis=1, keepdims=True) + 1e-10
        )

        similarities = chunk_norms @ jd_norm
        top_k = min(5, len(similarities))
        top_scores = np.sort(similarities)[::-1][:top_k]
        final_score = float(np.mean(top_scores) * 100)

        return round(max(0.0, min(final_score, 100.0)), 2)

    except Exception as e:
        print(f"compute_similarity ERROR: {e}")
        return 0.0


def process_candidates(files: List[str], jd: str) -> List[Dict]:
    results = []
    for file in files:
        try:
            text = load_resume(file)
            parsed = parse_resume(text)
            score = compute_similarity(jd, text)
            results.append({
                "name": parsed.get("name", "Unknown"),
                "score": score,
                "skills": parsed.get("skills", []),
                "experience": parsed.get("experience", "N/A"),
                "education": parsed.get("education", "N/A"),
                "summary": parsed.get("summary", "N/A"),
            })
        except Exception as e:
            print(f"process_candidates ERROR for {file}: {e}")
            results.append({
                "name": "Unknown",
                "score": 0.0,
                "skills": [],
                "experience": "N/A",
                "education": "N/A",
                "summary": "N/A",
            })

    return sorted(results, key=lambda x: x["score"], reverse=True)
