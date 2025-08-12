import sys
import os

# Add the current directory to Python path to import from utils
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from utils.auth import LLM
import base64

obj = LLM(r"/home/chandrahaas/codes/Bot/.env")

with open(r"/home/chandrahaas/codes/Bot/prompts/ScreenShot.md", 'r') as f:
    prompt = f.read()

q = """Request to need your help RM created 2time login fee link created 
but one was an error and the delete option was not showing please resolve this issue
Customer name - Kavitha R
Branch Name - Kunigal
Emp ID - SF0425"""

prompt = obj.format_prompt('{not_provided}', q, prompt, False)
#print(obj.get_gemini_response(prompt))

img_path = r"/home/chandrahaas/codes/Bot/unnamed.jpg"

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

base64_string = encode_image_to_base64(img_path)

# Use the new multimodal method that properly handles images
print("Sending prompt with image to Gemini...")
response = obj.get_gemini_response_with_image(prompt, img_path)
print("Gemini Response:")
print(response)