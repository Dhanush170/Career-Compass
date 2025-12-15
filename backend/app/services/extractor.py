import os
import shutil
from unstract.llmwhisperer import LLMWhispererClientV2
from app.config import LLMWHISPERER_API_KEY

client = LLMWhispererClientV2(api_key=LLMWHISPERER_API_KEY)

def extract_text_from_pdf(upload_file) -> str:
    # 1. Save the upload temporarily
    temp_path = f"temp_{upload_file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    
    try:
        # 2. Call LLMWhisperer
        res = client.whisper(
            file_path=temp_path,
            mode="high_quality",
            wait_for_completion=True,
            horizontal_stretch_factor="1.05"
        )
        return res["extraction"]["result_text"]
    except Exception as e:
        print(f"Extraction Error: {e}")
        return ""
    finally:
        # 3. Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)