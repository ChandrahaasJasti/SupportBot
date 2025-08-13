
class ContextManager:
    
    def __init__(self):
        self.context=[]
        print("ContextManager initialized")

    def format_context(self):
        context_str=""
        for i in self.context:
            context_str+=f"user_query: {i['user_query']}\nagent_response: {i['agent_response']}\n"
        return context_str

    def get_context(self):
        return self.format_context()

    def add_context(self,user_query,agent_response):
        self.context.append({"user_query":user_query,"agent_response":agent_response})

    