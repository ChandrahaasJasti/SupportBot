import sys
import os
import json
from utils.agent import Agent
agent=Agent()
img_path=r"/home/chandrahaas/codes/Bot/unnamed.jpg"
user_query="i generated the payment link twice and the customer paid through the second link, its showing like this. But the next process is not starting"
executer=agent.start_agent(user_query,None,True,img_path)
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
print("EXECUTER")
print(executer)
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

# current_dir = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, current_dir)
# from utils.rag import EmbRag
# obj=EmbRag(docs_path=r"/home/chandrahaas/codes/Bot/DOCS",faiss_path=r"/home/chandrahaas/codes/Bot/Faiss")
# print(obj.queryDB("I am not getting an OTP , what to do"))
