from .rag import EmbRag
from .auth import LLM
DOCS_PATH=r"/home/chandrahaas/codes/Bot/DOCS"
FAISS_PATH=r"/home/chandrahaas/codes/Bot/FAISS"


class Agent:
    def __init__(self):
        self.rag=EmbRag(DOCS_PATH,FAISS_PATH)