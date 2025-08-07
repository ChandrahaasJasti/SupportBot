from dotenv import load_dotenv
import os

class Auth:
    def __init__(self,env_path):
        load_dotenv(dotenv_path=env_path)
        self.api_key=os.getenv("GEMINI")
        from google import genai
        load_dotenv(dotenv_path=env_path)
        self.__gemini_client = genai.Client(api_key=self.api_key)

    def get_gemini_client(self):
        return self.__gemini_client
        


class LLM:
    def __init__(self,env_path):
        self.auth_obj=Auth(env_path)
        self.gemini_client=self.auth_obj.get_gemini_client()
    
    def format_prompt(self,replacer,user_input,system_prompt,isPath=False):
        if(isPath==True):
            with open(system_prompt,'r') as f:
                system_prompt=f.read()
        system_prompt=system_prompt.replace(replacer,user_input)
        return system_prompt

    def get_gemini_response(self,prompt):
        response = self.gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text


        #self.api_key=os.getenv("GEMINI")

