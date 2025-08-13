import faiss
import os
from pathlib import Path
import json
from trafilatura import fetch_url, extract
import pymupdf4llm
import numpy as np 
import requests
from .auth import LLM
ENV_PATH=r"/home/chandrahaas/codes/Bot/.env"
""" things remaining : chunker,faiss """
class EmbRag:
    def __init__(self,docs_path,faiss_path):
        """faiss index creation"""
        self.llm_obj=LLM(ENV_PATH)
        index_path =Path(faiss_path+"/index.bin")
        if(index_path.exists()):
            index=faiss.read_index(str(index_path))
        else:
            index=faiss.IndexFlatL2(768)
        self.docs=docs_path
        self.faiss_path=faiss_path
        flag=True
        self.pth=os.path.join(faiss_path,"cache.json")
        self.pth2=os.path.join(faiss_path,"meta_data.json")
        self.pth_checker1(self.pth2)
        self.pth_checker(self.pth)
        with open(self.pth,'r') as f:
            self.cache=json.load(f)
        self.files=os.listdir(docs_path)
        with open(self.pth2,'r') as f:
            self.chunks=f.read()
        l=eval(self.chunks)
        for i in self.files:
            if i not in self.cache:
                if((i.endswith('.txt') or i.endswith('.md')) and not i.startswith('url')):
                    with open(os.path.join(self.docs,i),'r') as f:
                        text=f.read()
                    chunks=self.chunk_text(text)
                    embeds=[]
                    for k in range(len(chunks)):
                        dic={}
                        dic['doc']=i
                        dic['id']=k
                        dic['content']=chunks[k]
                        l.append(dic)
                        embeds.append(self.get_embedding(chunks[k]))
                    ans=np.stack(embeds)
                    index.add(ans)
                    #l.append(chk ) append all the chunks to this list

                elif(i.endswith('.pdf')):
                    md_text = pymupdf4llm.to_markdown(os.path.join(self.docs,i))
                    chunks=self.chunk_text(md_text)
                    embeds=[]
                    for k in range(len(chunks)):
                        dic={}
                        dic['doc']=i
                        dic['id']=k
                        dic['content']=chunks[k]
                        l.append(dic)
                        embeds.append(self.get_embedding(chunks[k]))
                    ans=np.stack(embeds)
                    index.add(ans)
                elif(i.endswith('.txt') and i.startswith('url')):
                    with open(os.path.join(self.docs,i),'r') as f:
                        links=f.read()
                        self.urls=links.split(',')
                    chunks=[]
                    for j in self.urls:
                        downloaded = fetch_url(j)
                        result = extract(downloaded)
                        if result is None:
                            print(f"could not access the url {j} because of authentication ")
                        else:
                            chunks.append(result)
                            l.append({'doc': f"url{j}", "content": result})
                    embeds = []
                    for k in range(len(chunks)):
                        dic = {}
                        dic['doc'] = i
                        dic['id'] = k
                        dic['content'] = chunks[k]
                        l.append(dic)
                        embeds.append(self.get_embedding(chunks[k]))
                    ans=np.stack(embeds)
                    index.add(ans)

                else:
                    flag=False
                    print(f"{i} is not a part of [pdf,txt,website] markitdown feature coming soon")
                self.cache[i]="True"
        with open(self.pth,'w') as f:
            json.dump(self.cache,f,indent=4)
        with open(self.pth2,'w') as f:
            json.dump(l,f,indent=4)
        faiss.write_index(index, str(index_path))
    
    def pth_checker(self,arge):
        file_path=Path(arge)
        if(not file_path.exists()):
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path,'w') as f:
                json.dump({},f)
    
    def pth_checker1(self,arge):
        file_path=Path(arge)
        if(not file_path.exists()):
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path,'w') as f:
                json.dump([],f)

    def chunk_text_depricated(self,text):
        WORD_COUNT = 512
        OVERLAP = 50
        
        # Split text into words
        words = text.split()
        chunks = []
        
        # Calculate the step size (chunk size - overlap)
        step = WORD_COUNT - OVERLAP
        
        # Create chunks with overlap
        for i in range(0, len(words), step):
            # Get the chunk of words
            chunk = words[i:i + WORD_COUNT]
            
            # Only add chunk if it's not empty
            if chunk:
                # Join words back into text
                chunk_text = ' '.join(chunk)
                chunks.append(chunk_text)
                
                # If we've reached the end of the text, break
                if i + WORD_COUNT >= len(words):
                    break
        
        return chunks

    def chunk_text(self,text):
        """
        Chunk text into 256-word blocks using LLM-based topic detection.
        
        Strategy:
        1. Slice input into 256-word blocks
        2. Ask LLM if there's a second topic in the block
        3. If second topic found, split at that point
        4. First part becomes finalized chunk, second part prepended to next block
        5. Continue recursively until entire document is processed
        
        Args:
            text (str): Input text to be chunked
            
        Returns:
            list: List of text chunks
        """
        def split_into_words(text):
            """Split text into words for counting"""
            return text.split()
        
        def join_words(words):
            """Join words back into text"""
            return ' '.join(words)
        
        def get_second_topic_part(block_text):
            """Ask LLM if there's a second topic and return the second part if found"""
            prompt = f"""
            Analyze this text block and determine if it contains a second distinct topic.
            
            Text block:
            {block_text}
            
            If there is a second topic in this block, return ONLY the text from where the second topic begins (including that sentence).
            If there is only one topic throughout the block, return "NO_SECOND_TOPIC".
            
            Be precise and only return the actual text of the second topic part, or "NO_SECOND_TOPIC".
            """
            
            response = self.llm_obj.get_gemini_response(prompt)
            
            # Check if LLM found a second topic
            if response.strip() == "NO_SECOND_TOPIC":
                return None
            else:
                # Return the second topic part
                return response.strip()
        
        chunks = []
        words = split_into_words(text)
        current_position = 0
        
        while current_position < len(words):
            # Get next 256-word block
            end_position = min(current_position + 256, len(words))
            current_block_words = words[current_position:end_position]
            current_block_text = join_words(current_block_words)
            
            # Ask LLM if there's a second topic
            second_topic_part = get_second_topic_part(current_block_text)
            
            if second_topic_part is None:
                # No second topic found, this is a complete chunk
                chunks.append(current_block_text)
                current_position = end_position
            else:
                # Second topic found, need to split
                # Find where the second topic starts in the current block
                second_topic_words = split_into_words(second_topic_part)
                
                # Find the position where second topic starts
                # We need to find the overlap between current block and second topic
                first_part_words = []
                for i, word in enumerate(current_block_words):
                    # Check if remaining words match the start of second topic
                    remaining_words = current_block_words[i:]
                    if len(remaining_words) >= len(second_topic_words):
                        # Check if the remaining words start with second topic words
                        if remaining_words[:len(second_topic_words)] == second_topic_words:
                            first_part_words = current_block_words[:i]
                            break
                
                # If we couldn't find the split point, use a fallback
                if not first_part_words:
                    # Fallback: split at roughly 75% of the block
                    split_point = int(len(current_block_words) * 0.75)
                    first_part_words = current_block_words[:split_point]
                    second_topic_words = current_block_words[split_point:]
                
                # Add the first part as a finalized chunk
                if first_part_words:
                    chunks.append(join_words(first_part_words))
                
                # Prepend the second part to the next block
                # Move position to where first part ended
                current_position += len(first_part_words)
                
                # If we're at the end, add the remaining part as the last chunk
                if current_position >= len(words):
                    if second_topic_words:
                        chunks.append(join_words(second_topic_words))
                    break
        
        return chunks
    
    def get_embedding_depricated(self,text):
        response = requests.post(
            "http://localhost:11434/api/embeddings",
            json={
                "model": "nomic-embed-text",
                "prompt": text
            }
        )
        response.raise_for_status()
        return np.array(response.json()["embedding"], dtype=np.float32)

    def get_embedding(self, text):
        """
        Gets an embedding for the given text from Ollama's nomic-embed-text model
        and L2-normalizes it.
        """
        response = requests.post(
            "http://localhost:11434/api/embeddings",
            json={
                "model": "nomic-embed-text",
                "prompt": text
            }
        )
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)

        # Get the raw embedding as a NumPy array
        embedding = np.array(response.json()["embedding"], dtype=np.float32)

        # Calculate the L2 norm
        norm = np.linalg.norm(embedding)

        # L2 Normalize the embedding. Handle zero norm to prevent division by zero.
        if norm == 0:
            return embedding # Return as is if it's a zero vector
        else:
            return embedding / norm
    
    def queryEnhancer(self,user_input,context_obj):
        context=context_obj.get_context()
        system_prompt_path=r"/home/chandrahaas/codes/Bot/prompts/QueryEnhancer.md"
        full_prompt=self.llm_obj.format_prompt('{replace_with_query}',user_input,system_prompt_path,isPath=True)
        full_prompt=self.llm_obj.format_prompt('{replace_with_context}',str(context),full_prompt)
        return self.llm_obj.get_gemini_response(full_prompt)

    def summarizer(self,relevancy,user_query,context):
        system_prompt_path=r"/home/chandrahaas/codes/Bot/prompts/Summariser.md"
        prompt=self.llm_obj.format_prompt('{replace_with_relevancy_score}',relevancy,system_prompt_path,isPath=True)
        prompt=self.llm_obj.format_prompt('{replace_with_context}',str(context),prompt)
        prompt=self.llm_obj.format_prompt('{replace_with_user_query}',user_query,prompt)
        return self.llm_obj.get_gemini_response(prompt)

    def queryDB(self,q):
        initial_q=q
        q=self.queryEnhancer(q)
        vec=self.get_embedding(q).reshape(1,-1)
        index_path =Path(self.faiss_path+"/index.bin")
        if(index_path.exists()):
            index=faiss.read_index(str(index_path))
            D,I=index.search(vec,k=3)
            with open(self.pth2,'r') as f:
                lst=f.read()
            lst=eval(lst)
            indices=I[0]
            distances=D[0]
            ans=[]
            RELEVANCY="good"
            for i in range(len(indices)):

                if indices[i]!=-1 and distances[i]<2.0:    
                    dic=lst[indices[i]]
                    content=dic['content']
                    ans.append(content)
                    if(distances[i]>1):
                        RELEVANCY="bad"
            #print(RELEVANCY)
            print(ans)
            return self.summarizer(RELEVANCY,initial_q,ans)
        else:
            print("no faiss index found")
            ans=[]
            return ans