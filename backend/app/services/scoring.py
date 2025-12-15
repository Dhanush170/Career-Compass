# backend/app/services/scoring.py

import re
import math
import numpy as np
from typing import List, Tuple, Dict, Any
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import util

# --- LOCAL IMPORTS ---
from app.services.ai_models import ai_loader
from app.data.skills import TECH_SKILLS, ALIASES, FLAT_SKILLS

# --- CONSTANTS ---
JD_STOP_PHRASES = {
    "role offers", "customer facing role", "software industry",
    "organization position require", "requirements deliver project",
    "role requires strong", "adapt dynamic business", "global services team",
    "experience providing technical",
}

JD_STOP_WORDS = {
    "role", "offers", "experience", "position", "require", "requirements",
    "project", "business", "team", "services", "dynamic", "global", "based",
}

# --- 1. HELPER UTILITIES ---
def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())

def _clean_lower(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip().lower())

def _chunk_text(text: str, max_len: int = 256) -> List[str]:
    text = _clean_lower(text)
    sents = re.split(r"[.\n;]", text)
    chunks, cur = [], ""
    for s in sents:
        s = s.strip()
        if not s: continue
        if len(cur) + len(s) < max_len:
            cur += (" " + s) if cur else s
        else:
            if cur: chunks.append(cur)
            cur = s
    if cur: chunks.append(cur)
    return chunks

# --- 2. EXTRACTION LOGIC ---
def extract_jd_phrases(jd_text: str, top_k: int = 25) -> List[str]:
    jd_text = _clean(jd_text)
    if not jd_text: return []
    
    # USE SINGLETON MODEL
    kw_model = ai_loader.kw_model 
    
    kw_scores = kw_model.extract_keywords(
        jd_text, keyphrase_ngram_range=(1, 2), stop_words="english",
        use_mmr=True, diversity=0.3, top_n=top_k, nr_candidates=80,
    )
    cleaned, seen = [], set()
    for kw, _ in kw_scores:
        k = kw.lower().strip()
        if not k or k in JD_STOP_PHRASES or len(k) < 3 or k in seen: continue
        tokens = k.split()
        if any(tok in JD_STOP_WORDS for tok in tokens):
            if not (len(tokens) == 2 and not any(t in JD_STOP_WORDS for t in tokens)): continue
        seen.add(k)
        cleaned.append(k)
    return cleaned

def extract_tech_keywords(text: str) -> Dict[str, List[str]]:
    norm = _clean_lower(text)
    found = {cat: set() for cat in TECH_SKILLS.keys()}
    found["other"] = set()
    for skill, cat in FLAT_SKILLS.items():
        pattern = r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])"
        if re.search(pattern, norm):
            canon = ALIASES.get(skill, skill)
            canonical_cat = None
            for c, items in TECH_SKILLS.items():
                if canon in items:
                    canonical_cat = c
                    break
            found[canonical_cat or cat].add(canon)
    return {cat: sorted(list(vals)) for cat, vals in found.items() if vals}

def flatten_skills(tech_dict: Dict[str, List[str]]) -> List[str]:
    out = []
    for vals in tech_dict.values(): out.extend(vals)
    return sorted(set(out))

# --- 3. PRESENCE CHECK ---
def check_presence(keywords: List[str], resume_text: str, sim_threshold: float = 0.6) -> Dict[str, Any]:
    resume_clean = _clean_lower(resume_text)
    if not keywords or not resume_clean:
        return {"score": 0.0, "matched_count": 0, "total": len(keywords), "matched": [], "unmatched": keywords, "details": []}

    chunks = _chunk_text(resume_text)
    if not chunks: return {"score": 0.0, "matched_count": 0, "total": len(keywords), "matched": [], "unmatched": keywords, "details": []}

    # USE SINGLETON MODEL
    sentence_model = ai_loader.sentence_model
    chunk_emb = sentence_model.encode(chunks)
    
    matched, unmatched, details = [], [], []

    for kw in keywords:
        kw_l = kw.lower().strip()
        if not kw_l: continue

        # Exact
        if kw_l in resume_clean:
            matched.append(kw)
            details.append({"keyword": kw, "match_type": "exact", "similarity": 1.0, "snippet": "substring"})
            continue

        # Token
        tokens = [t for t in re.split(r"\W+", kw_l) if t]
        important = [t for t in tokens if t not in {"development", "skills", "experience", "role", "model", "concepts"}] or tokens
        if any(tok in resume_clean for tok in important):
            matched.append(kw)
            details.append({"keyword": kw, "match_type": "token", "similarity": 1.0, "snippet": "token match"})
            continue

        # Semantic
        kw_emb = sentence_model.encode([kw_l])
        sims = cosine_similarity(kw_emb, chunk_emb)[0]
        best_idx = int(np.argmax(sims))
        best_sim = float(sims[best_idx])
        thresh = max(sim_threshold - 0.05, 0.5) if len(tokens) <= 2 else sim_threshold
        
        if best_sim >= thresh:
            matched.append(kw)
            details.append({"keyword": kw, "match_type": "semantic", "similarity": round(best_sim, 3), "snippet": chunks[best_idx][:200]})
        else:
            unmatched.append(kw)

    score = (len(matched) / len(keywords)) * 100 if keywords else 0.0
    return {"score": round(score, 2), "matched_count": len(matched), "total": len(keywords), "matched": matched, "unmatched": unmatched, "details": details}

# --- 4. SCORING FUNCTIONS ---
def calculate_semantic_score(res_text, jd_text):
    try:
        model = ai_loader.sentence_model
        e1 = model.encode(res_text, convert_to_tensor=True)
        e2 = model.encode(jd_text, convert_to_tensor=True)
        return round(max(0, min(util.cos_sim(e1, e2).item() * 100, 100)), 2)
    except: return 0

def calculate_format_score(resume_text):
    score = 0
    text = resume_text.lower()
    if re.search(r'[\w\.-]+@[\w\.-]+', text): score += 10
    if re.search(r'\d{10}', text) or re.search(r'\+\d{1,3}', text): score += 10
    required = ["education", "experience", "skills", "projects"]
    score += (sum([1 for s in required if s in text]) * 10)
    if re.search(r'^\s*[\u2022\u2023\u25E6\u2043\u2219\-*]', resume_text, re.MULTILINE): score += 20
    wc = len(text.split())
    if 300 <= wc <= 1200: score += 20
    elif wc > 1200: score += 10
    return min(score, 100)

def calculate_experience_score(resume_text):
    score = 0
    text_lower = resume_text.lower()
    if "internships" in text_lower or "experience" in text_lower: score += 30
    if "project" in text_lower: score += 20
    strong_verbs = ["analyzed", "built", "created", "designed", "developed", "led", "managed", "optimized"]
    verb_count = sum([1 for w in text_lower.split() if w in strong_verbs])
    score += min(verb_count * 2, 50)
    return min(score, 100)

# --- 5. ORCHESTRATORS ---
def evaluate_jd_resume(jd_text: str, resume_text: str, top_k_jd=20, sim_threshold=0.6):
    jd_phrases = extract_jd_phrases(jd_text, top_k=top_k_jd)
    jd_phrase_pres = check_presence(jd_phrases, resume_text, sim_threshold=sim_threshold)
    
    jd_tech_flat = flatten_skills(extract_tech_keywords(jd_text))
    resume_tech_flat = flatten_skills(extract_tech_keywords(resume_text))
    tech_pres = check_presence(jd_tech_flat, resume_text, sim_threshold=sim_threshold)
    
    w_tech, w_jd = 0.6, 0.4
    if jd_tech_flat and jd_phrases: overall = w_tech * tech_pres["score"] + w_jd * jd_phrase_pres["score"]
    elif jd_tech_flat: overall = tech_pres["score"]
    elif jd_phrases: overall = jd_phrase_pres["score"]
    else: overall = 0.0
    
    return {
        "jd_phrases": jd_phrases, "jd_phrase_presence": jd_phrase_pres,
        "jd_tech_flat": jd_tech_flat, "tech_presence": tech_pres,
        "resume_tech_flat": resume_tech_flat,
        "resume_only_tech": sorted(set(resume_tech_flat) - set(jd_tech_flat)),
        "scores": {"overall_keyword_score": round(overall, 2)}
    }

def calculate_keyword_score(resume_text: str, jd_text: str) -> Dict:
    if not jd_text.strip() and not resume_text.strip(): return {"keyword_score": 0.0, "missing_skills": []}
    eval_res = evaluate_jd_resume(jd_text, resume_text)
    
    tech_un = eval_res["tech_presence"]["unmatched"]
    phrase_un = eval_res["jd_phrase_presence"]["unmatched"]
    combined_missing = list(dict.fromkeys(tech_un + phrase_un))[:5]
    
    return {
        "keyword_score": eval_res["scores"]["overall_keyword_score"],
        "missing_skills": combined_missing,
        "details": eval_res # Pass full details if needed
    }

# --- MAIN EXPORT ---
def calculate_ats_analysis(resume_text: str, jd_text: str) -> Dict[str, Any]:
    sem = float(calculate_semantic_score(resume_text, jd_text))
    fmt = float(calculate_format_score(resume_text))
    exp = float(calculate_experience_score(resume_text))
    kw_data = calculate_keyword_score(resume_text, jd_text)
    
    kw_score = float(kw_data["keyword_score"])
    weights = {"keyword": 0.4, "semantic": 0.3, "format": 0.2, "experience": 0.1}
    final_score = round(
        weights["keyword"] * kw_score + 
        weights["semantic"] * sem + 
        weights["format"] * fmt + 
        weights["experience"] * exp, 1
    )
    
    # Band
    if final_score >= 85: band = "Excellent Match"
    elif final_score >= 70: band = "Strong Match"
    elif final_score >= 55: band = "Moderate Match"
    else: band = "Weak Match"
    
    # Suggestion
    suggestion = f"Current resume has a {band} ({final_score}). "
    if kw_data["missing_skills"]:
        suggestion += f"Add skills like: {', '.join(kw_data['missing_skills'][:3])}."
    elif fmt < 60:
        suggestion += "Focus on improving your formatting and section headers."
    
    return {
        "ats_score": final_score,
        "ats_band": band,
        "suggestion": suggestion,
        "scores": {
            "keyword_score": kw_score,
            "semantic_score": sem,
            "format_score": fmt,
            "experience_score": exp
        },
        "missing_skills": kw_data["missing_skills"],
        "meta": {
            "resume_word_count": len(resume_text.split()),
            "jd_word_count": len(jd_text.split())
        }
    }