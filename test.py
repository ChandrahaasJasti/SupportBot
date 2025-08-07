from rag import EmbRag
DOCS=r"/home/chandrahaas/codes/test-apis/Bot/DOCS"
FAISS=r"/home/chandrahaas/codes/test-apis/Bot/Faiss"

print("Enter Your Queiries")
print("you can exit if you type EXIT")
while(True):
    emb_rag_obj=EmbRag(DOCS,FAISS)
    q=str(input())
    if(q=="EXIT"):
        break
    else:
        print(emb_rag_obj.queryDB(q))
#print(emb_rag_obj.queryDB("what is Vivek Bansal responsible for?"))
# from utils.auth import LLM

# obj=LLM(r"/home/chandrahaas/codes/test-apis/Bot/.env")
# with open(r"/home/chandrahaas/codes/test-apis/Bot/prompts/QueryEnhancer.md",'r') as f:
#     prompt=f.read()
# q="who is Chandrahaas Jasti? I think he works at Saarathi Finance"
# prompt=obj.format_prompt('{replace_with_query}',q,r"/home/chandrahaas/codes/test-apis/Bot/prompts/QueryEnhancer.md",True)
# #print(prompt)
# print(obj.get_gemini_response(prompt))



# llm_obj=LLM(r"/home/chandrahaas/codes/test-apis/Bot/.env")
# #print(llm_obj.get_gemini_response("Explain how AI works in a few words"))

# def chunk_text(text):
#     """
#     Chunk text into 256-word blocks using LLM-based topic detection.
    
#     Strategy:
#     1. Slice input into 256-word blocks
#     2. Ask LLM if there's a second topic in the block
#     3. If second topic found, split at that point
#     4. First part becomes finalized chunk, second part prepended to next block
#     5. Continue recursively until entire document is processed
    
#     Args:
#         text (str): Input text to be chunked
        
#     Returns:
#         list: List of text chunks
#     """
#     def split_into_words(text):
#         """Split text into words for counting"""
#         return text.split()
    
#     def join_words(words):
#         """Join words back into text"""
#         return ' '.join(words)
    
#     def get_second_topic_part(block_text):
#         """Ask LLM if there's a second topic and return the second part if found"""
#         prompt = f"""
#         Analyze this text block and determine if it contains a second distinct topic.
        
#         Text block:
#         {block_text}
        
#         If there is a second topic in this block, return ONLY the text from where the second topic begins (including that sentence).
#         If there is only one topic throughout the block, return "NO_SECOND_TOPIC".
        
#         Be precise and only return the actual text of the second topic part, or "NO_SECOND_TOPIC".
#         """
        
#         response = llm_obj.get_gemini_response(prompt)
        
#         # Check if LLM found a second topic
#         if response.strip() == "NO_SECOND_TOPIC":
#             return None
#         else:
#             # Return the second topic part
#             return response.strip()
    
#     chunks = []
#     words = split_into_words(text)
#     current_position = 0
    
#     while current_position < len(words):
#         # Get next 256-word block
#         end_position = min(current_position + 256, len(words))
#         current_block_words = words[current_position:end_position]
#         current_block_text = join_words(current_block_words)
        
#         # Ask LLM if there's a second topic
#         second_topic_part = get_second_topic_part(current_block_text)
        
#         if second_topic_part is None:
#             # No second topic found, this is a complete chunk
#             chunks.append(current_block_text)
#             current_position = end_position
#         else:
#             # Second topic found, need to split
#             # Find where the second topic starts in the current block
#             second_topic_words = split_into_words(second_topic_part)
            
#             # Find the position where second topic starts
#             # We need to find the overlap between current block and second topic
#             first_part_words = []
#             for i, word in enumerate(current_block_words):
#                 # Check if remaining words match the start of second topic
#                 remaining_words = current_block_words[i:]
#                 if len(remaining_words) >= len(second_topic_words):
#                     # Check if the remaining words start with second topic words
#                     if remaining_words[:len(second_topic_words)] == second_topic_words:
#                         first_part_words = current_block_words[:i]
#                         break
            
#             # If we couldn't find the split point, use a fallback
#             if not first_part_words:
#                 # Fallback: split at roughly 75% of the block
#                 split_point = int(len(current_block_words) * 0.75)
#                 first_part_words = current_block_words[:split_point]
#                 second_topic_words = current_block_words[split_point:]
            
#             # Add the first part as a finalized chunk
#             if first_part_words:
#                 chunks.append(join_words(first_part_words))
            
#             # Prepend the second part to the next block
#             # Move position to where first part ended
#             current_position += len(first_part_words)
            
#             # If we're at the end, add the remaining part as the last chunk
#             if current_position >= len(words):
#                 if second_topic_words:
#                     chunks.append(join_words(second_topic_words))
#                 break
    
#     return chunks

# # Example usage and testing
# if __name__ == "__main__":
#     # Test with a sample text
#     sample_text = """
#     Artificial Intelligence (AI) is a branch of computer science that aims to create intelligent machines capable of performing tasks that typically require human intelligence. These tasks include learning, reasoning, problem-solving, perception, and language understanding. Machine learning, a subset of AI, enables computers to learn and improve from experience without being explicitly programmed. Deep learning, a type of machine learning, uses neural networks with multiple layers to process complex patterns in data. Natural Language Processing (NLP) is another important area of AI that focuses on enabling computers to understand, interpret, and generate human language. Computer vision allows machines to interpret and understand visual information from the world. Robotics combines AI with mechanical engineering to create intelligent machines that can interact with the physical world. Expert systems are AI programs that mimic the decision-making abilities of human experts in specific domains. AI applications are widespread, including virtual assistants like Siri and Alexa, recommendation systems on platforms like Netflix and Amazon, autonomous vehicles, medical diagnosis systems, and financial trading algorithms. The field continues to evolve rapidly with advancements in algorithms, computing power, and data availability.
    
#     Machine learning algorithms can be broadly categorized into supervised learning, unsupervised learning, and reinforcement learning. Supervised learning involves training a model on labeled data, where the correct output is provided for each input. Classification and regression are common supervised learning tasks. Unsupervised learning works with unlabeled data and aims to discover hidden patterns or structures. Clustering and dimensionality reduction are typical unsupervised learning techniques. Reinforcement learning involves an agent learning to make decisions by interacting with an environment and receiving rewards or penalties. Deep learning has revolutionized many AI applications by automatically learning hierarchical representations of data. Convolutional Neural Networks (CNNs) are particularly effective for image processing tasks, while Recurrent Neural Networks (RNNs) and their variants like LSTM and GRU are well-suited for sequential data such as text and speech. Transformers, introduced in 2017, have become the foundation for many modern NLP models including BERT, GPT, and T5. These models use attention mechanisms to process relationships between different parts of the input data.
#     """
    
#     print("Original text length (words):", len(sample_text.split()))
#     print("\nChunking text...")
    
#     chunks = chunk_text(sample_text)
    
#     for i in range(len(chunks)):
#         print(chunks[i])
#     # print(f"\nCreated {len(chunks)} chunks:")
#     # for i, chunk in enumerate(chunks, 1):
#     #     word_count = len(chunk.split())
#     #     print(f"\nChunk {i} ({word_count} words):")
#     #     print(chunk[:200] + "..." if len(chunk) > 200 else chunk)
