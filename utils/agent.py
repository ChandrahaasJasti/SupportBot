from .rag import EmbRag
from .auth import LLM
from .auth import AgentContextManager
import json
import re
ENV_PATH=r"/home/chandrahaas/codes/Bot/.env"
DOCS_PATH=r"/home/chandrahaas/codes/Bot/DOCS"
FAISS_PATH=r"/home/chandrahaas/codes/Bot/FAISS"


class Agent:
	def __init__(self):
		self.rag=EmbRag(DOCS_PATH,FAISS_PATH)
		self.llm=LLM(ENV_PATH)
		self.agent_context=AgentContextManager()
		self.log={}
	
	#PERCEPTION(extracts JSON from user query) -> DECISION(decides the agent to be used) -> EXECUTER(executes the query) or PLANNER(plans the next query) then EXECUTES
	def start_agent(self,user_query,user_context_obj,screen_shot=True,image_base64=None):
		if(screen_shot):
			perception=self.get_screen_perception(user_query,image_base64,user_context_obj)
		else:
			perception=self.get_perception(user_query,user_context_obj)
		self.log["perception"]=perception
		decision=self.get_decision(perception)
		self.log["decision"]=decision
		json_decision=decision if isinstance(decision, dict) else json.loads(decision)
		if(json_decision["agent"])=="executer":
			query=json_decision["query"]
			response=self.rag.queryDB(query)
			self.log["executer_response"]=response
			return response
		elif(json_decision["agent"])=="planner":
			plan=self.planner(json_decision["query"])
			plan=plan if isinstance(plan, dict) else json.loads(plan)
			self.log["planner_response"]=plan

			for i in plan:
				q=plan[i]
				step_response=self.rag.queryDB(q)
				self.agent_context.add_context(q,step_response)
			context=self.agent_context.get_context()
			response=self.summariser(context)
		self.log["planned_outputs"]=self.agent_context.context
		self.log["final_response"]=response
		with open(r"",'w') as jw:
			json.dump(self.log,jw,indent=4)
		return response

	def _strip_code_fences(self, text):
		"""Remove leading ```json ... ``` or ``` ... ``` code fences and return inner content.
		- If input is dict/list, return as-is.
		- If no fenced block is found, return the trimmed text unchanged.
		"""
		if text is None:
			return text
		if isinstance(text, (dict, list)):
			return text
		# Coerce non-string to string safely
		if not isinstance(text, (str, bytes)):
			text=str(text)
		pattern = r"```\s*(?:json)?\s*([\s\S]*?)\s*```"
		match = re.search(pattern, text, flags=re.IGNORECASE)
		if match:
			return match.group(1).strip()
		return text.strip()

	def get_perception(self,user_query,user_context_obj=None):
		if(user_context_obj):
			context=user_context_obj.get_context()
		else:
			context="no_context"
		with open(r"prompts/Perception.md",'r') as pr:
			prompt=pr.read()
		if(context!="no_context"):
			prompt=self.llm.format_prompt(replacer="{no_context}",user_input=context,system_prompt=prompt)
		prompt=self.llm.format_prompt(replacer="{replace_with_query}",user_input=user_query,system_prompt=prompt)
		resp=self.llm.get_gemini_response(prompt)
		return resp

	def get_decision(self,perception):
		with open(r"prompts/Decision.md",'r') as pr:
			prompt=pr.read()
		# Ensure valid JSON string passed into the prompt
		#perception_str=json.dumps(perception, ensure_ascii=False)
		prompt=self.llm.format_prompt(replacer="{replace_with_perception_json}",user_input=perception,system_prompt=prompt)
		resp=self.llm.get_gemini_response(prompt)
		print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
		print("DECISION")
		print(resp)
		print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
		resp=self._strip_code_fences(resp)
		return json.loads(resp)
	
	def planner(self,query):
		prompt=""
		resp=self.llm.get_gemini_response(prompt)
		resp=self._strip_code_fences(resp)
		return json.loads(resp)
	
	def summariser(self,context):
		prompt=""
		resp=self.llm.get_gemini_response(prompt)
		resp=self._strip_code_fences(resp)
		return json.loads(resp)
	
	def get_screen_perception(self,user_query,image_base64,user_context_obj=None):
		if(user_context_obj):
			context=user_context_obj.get_context()
		else:
			context="no_context"
		with open(r"prompts/PerceptionSS.md",'r') as pr:
			prompt=pr.read()
		if(context!="no_context"):
			prompt=self.llm.format_prompt(replacer="{no_context}",user_input=context,system_prompt=prompt)
		prompt=self.llm.format_prompt(replacer="{replace_with_query}",user_input=user_query,system_prompt=prompt)
		resp=self.llm.get_gemini_response_with_image(prompt,image_base64)
		print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
		print("PERCEPTION")
		print(resp)
		print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
		return resp
				
