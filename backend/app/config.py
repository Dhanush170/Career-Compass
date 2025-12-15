import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
LLMWHISPERER_API_KEY = os.getenv("LLMWHISPERER_API_KEY")