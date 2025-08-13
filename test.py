import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
from utils.rag import EmbRag
obj=EmbRag(docs_path=r"/home/chandrahaas/codes/Bot/DOCS",faiss_path=r"/home/chandrahaas/codes/Bot/Faiss")
print(obj.queryDB("I am not getting an OTP , what to do"))