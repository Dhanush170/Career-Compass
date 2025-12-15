from sentence_transformers import SentenceTransformer
from keybert import KeyBERT

class AIModelLoader:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("Loading AI Models... (This happens only once)")
            cls._instance = super(AIModelLoader, cls).__new__(cls)
            # Load SBERT
            cls._instance.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
            # Load KeyBERT
            cls._instance.kw_model = KeyBERT(model=cls._instance.sentence_model)
            print("Models Loaded.")
        return cls._instance

# Global instance to import
ai_loader = AIModelLoader()