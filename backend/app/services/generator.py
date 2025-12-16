# backend/app/services/generator.py

import json
import time
import re  # Added for better cleaning
import google.generativeai as genai
from typing import Dict, Any, List, Optional, Tuple
from app.config import GOOGLE_API_KEY

# --- SETUP ---
genai.configure(api_key=GOOGLE_API_KEY)
llm_model = genai.GenerativeModel('gemini-2.5-flash')

# --- HELPERS ---
def get_raw_llm_response(prompt):
    response = llm_model.generate_content(prompt)
    return response.text

def _clean_json_text(text: str) -> str:
    """Removes markdown code blocks and whitespace."""
    # Remove ```json and ```
    text = re.sub(r"```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)
    return text.strip()

def _safe_json_loads(text: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    # 1. Clean Markdown
    cleaned_text = _clean_json_text(text)
    
    # 2. Try Direct Parse
    try:
        return json.loads(cleaned_text), None
    except:
        pass

    # 3. Try finding outer braces
    start = cleaned_text.find("{")
    end = cleaned_text.rfind("}")
    if start != -1 and end != -1:
        try:
            return json.loads(cleaned_text[start:end+1]), None
        except:
            pass
            
    return None, text

def _call_llm_with_retry(prompt: str, retries: int = 2) -> Tuple[Optional[Dict], str]:
    last_raw = ""
    for _ in range(retries + 1):
        try:
            raw = get_raw_llm_response(prompt)
            last_raw = raw.strip()
            parsed, _ = _safe_json_loads(last_raw)
            if parsed: return parsed, last_raw
            time.sleep(1)
        except Exception as e:
            print(f"LLM Error: {e}")
    return None, last_raw

# --- CORE GENERATORS ---
def predict_roles_llm(resume_text: str, jd_text: str = None) -> Dict:
    prompt = f"""
    CONTEXT:
    RESUME: {resume_text[:4000]}
    
    TASK: Output top 3 predicted roles for this candidate. The reason should be in 1-2 lines.
    RETURN JSON ONLY:
    {{
      "predicted_roles": [
        {{ "role": "str", "score": 0.0-1.0, "matched_skills": ["str"], "evidence": ["str"], "reason": "str" }}
      ]
    }}
    """
    parsed, raw = _call_llm_with_retry(prompt)
    return {"predicted_roles": parsed.get("predicted_roles", []) if parsed else [], "raw": raw}

def estimate_skill_levels_llm(resume_text: str, skills: List[str]) -> Dict:
    # Fallback if no skills provided
    if not skills:
        skills = ["Communication", "Problem Solving", "Technical Skills"]

    prompt = f"""
    RESUME: {resume_text[:3000]}
    SKILLS: {json.dumps(skills)}
    TASK: Estimate level (Beginner/Intermediate/Expert) for each skill based on resume.
    RETURN JSON ONLY:
    {{
      "skill_levels": [
        {{ "skill": "str", "level": "str", "confidence": 0.0-1.0, "evidence": ["str"] }}
      ]
    }}
    """
    parsed, raw = _call_llm_with_retry(prompt)
    return {"skill_levels": parsed.get("skill_levels", []) if parsed else [], "raw": raw}

def generate_booster_snippets_llm(resume_text: str, jd_text: str, missing_skills: List[str]) -> Dict:
    # CRITICAL FIX: If no missing skills, ask to improve generic areas
    is_generic = False
    if not missing_skills:
        missing_skills = ["Advanced Optimization", "System Design", "Leadership"]
        is_generic = True

    prompt = f"""
    RESUME: {resume_text[:3000]}
    JD: {jd_text[:2000]}
    MISSING_SKILLS: {json.dumps(missing_skills)}
    
    TASK: Create resume bullet points for the MISSING_SKILLS.
    If the resume has NO evidence for a skill, mark 'derived_from_resume': false.
    {"Note: These are generic improvements." if is_generic else ""}
    
    RETURN JSON ONLY:
    {{
      "booster_suggestions": [
        {{ "skill": "str", "snippet": "str", "derived_from_resume": bool }}
      ]
    }}
    """
    parsed, raw = _call_llm_with_retry(prompt)
    return {"booster_suggestions": parsed.get("booster_suggestions", []) if parsed else [], "raw": raw}

def build_learning_path_llm(role: str, missing: List[str]) -> Dict:
    # CRITICAL FIX: If missing list is empty, default to general role improvement
    context_str = json.dumps(missing) if missing else "General Advanced Skills"

    prompt = f"""
    ROLE: {role}
    FOCUS_AREAS: {context_str}
    TASK: Create a 5-step learning path to master this role and gaps.
    RETURN JSON ONLY:
    {{
      "learning_path": [
        {{ "step": int, "title": "str", "duration_weeks": float, "type": "course|project", "notes": "str" }}
      ]
    }}
    """
    parsed, raw = _call_llm_with_retry(prompt)
    return {"learning_path": parsed.get("learning_path", []) if parsed else [], "raw": raw}

def suggest_future_trends_llm(role: str) -> Dict:
    prompt = f"""
    ROLE: {role}
    TASK: Suggest 3 future trends in 2-3 lines only.
    RETURN JSON ONLY:
    {{
      "future_trends": [
        {{ "name": "str", "why": "str" }}
      ]
    }}
    """
    parsed, raw = _call_llm_with_retry(prompt)
    return {"future_trends": parsed.get("future_trends", []) if parsed else [], "raw": raw}

# --- ORCHESTRATOR ---
def run_all_and_normalize(resume_text: str, jd_text: str, missing_skills: List[str]) -> Dict:
    # 1. Roles
    roles_data = predict_roles_llm(resume_text, jd_text)
    roles = roles_data.get("predicted_roles", [])
    primary_role = roles[0]["role"] if roles else "Software Engineer"
    
    # 2. Skill Levels 
    # Logic: Combine matched skills from prediction + missing skills to get a good mix
    skills_to_check = []
    for r in roles: 
        skills_to_check.extend(r.get("matched_skills", []))
    
    # Cap skills to check to avoid huge prompt
    skills_to_check = list(set(skills_to_check))[:10]
    # If empty, use defaults inside the function
    levels_data = estimate_skill_levels_llm(resume_text, skills_to_check)
    
    # 3. Boosters
    # Pass missing skills; function handles empty list logic
    boosters_data = generate_booster_snippets_llm(resume_text, jd_text, missing_skills[:5])
    
    # 4. Learning
    learn_data = build_learning_path_llm(primary_role, missing_skills[:5])
    
    # 5. Trends
    trends_data = suggest_future_trends_llm(primary_role)
    
    return {
        "predicted_roles": roles,
        "skill_levels": levels_data.get("skill_levels", []),
        "booster_suggestions": boosters_data.get("booster_suggestions", []),
        "learning_path": learn_data.get("learning_path", []),
        "future_trends": trends_data.get("future_trends", [])
    }

def build_ui_payload(combined: Dict) -> Dict:
    # Clean up structure for Frontend
    roles = combined.get("predicted_roles", [])
    return {
        "roles": roles,
        "primary_role": roles[0]["role"] if roles else "Software Engineer",
        "skill_levels": combined.get("skill_levels", []),
        "booster_suggestions": combined.get("booster_suggestions", []),
        "learning_path": combined.get("learning_path", []),
        "future_trends": combined.get("future_trends", [])
    }