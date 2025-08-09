import sys
import os

# Add the main Bot directory to the Python path
# This allows importing from utils and other packages
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now you can import from utils like:
from utils.rag import EmbRag
from utils.auth import LLM
DOCS=r"/home/chandrahaas/codes/Bot/DOCS"
FAISS=r"/home/chandrahaas/codes/Bot/Faiss"
obj=EmbRag(DOCS,FAISS)
print(obj.queryDB("How to download payslip?"))