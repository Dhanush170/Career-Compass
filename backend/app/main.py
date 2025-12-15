from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.services.extractor import extract_text_from_pdf
from app.services.scoring import calculate_ats_analysis
# CHANGE 1: Import 'build_ui_payload'
from app.services.generator import run_all_and_normalize, build_ui_payload 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(resume_file: UploadFile = File(...), jd_text: str = Form(...)):
    try:
        # 1. Extract
        print("Extracting PDF...")
        resume_text = extract_text_from_pdf(resume_file)
        if not resume_text:
            raise HTTPException(status_code=400, detail="Failed to extract text from PDF")
        
        # 2. Score (Math)
        print("Scoring...")
        ats_result = calculate_ats_analysis(resume_text, jd_text)
        
        # 3. Generate (LLM)
        print("Generating Advice...")
        llm_result_raw = run_all_and_normalize(resume_text, jd_text, ats_result["missing_skills"])
        
        # CHANGE 2: Convert raw LLM data to UI-friendly format
        # This converts 'predicted_roles' -> 'roles' so the Frontend doesn't crash
        llm_result_clean = build_ui_payload(llm_result_raw)
        
        # 4. Merge & Return
        return {**ats_result, **llm_result_clean}

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)