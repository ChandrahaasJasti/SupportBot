from .rag import EmbRag
from .auth import LLM
ENV_PATH=r"/home/chandrahaas/codes/Bot/.env"
DOCS_PATH=r"/home/chandrahaas/codes/Bot/DOCS"
FAISS_PATH=r"/home/chandrahaas/codes/Bot/FAISS"


class Agent:
    def __init__(self):
        self.rag=EmbRag(DOCS_PATH,FAISS_PATH)
        self.llm=LLM(ENV_PATH)

    def start_agent(self,user_query,screen_shot=True,image_base64=None):
        if(screen_shot):
            perception=self.get_screen_perception(user_query,image_base64)
        else:
            perception=self.get_perception(user_query)
        decision=self.get_decision(perception)
        json_decision=eval(decision)
        if(json_decision["agent"]=="executer"):