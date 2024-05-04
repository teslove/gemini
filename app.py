%%writefile app.py

import streamlit as st
from pathlib import Path
import google.generativeai as genai

genai.configure(api_key="AIzaSyBz3OcS81G4GEpCQvVWMbuxENBPnC9EGco")

# Set up the model

generation_config = {

"temperature": 0.4,

"top_p": 1,

"top_k": 32,

"max_output_tokens": 4096,

}

safety_settings = [

{

"category": "HARM_CATEGORY_HARASSMENT",

"threshold": "BLOCK_MEDIUM_AND_ABOVE"

},

{

"category": "HARM_CATEGORY_HATE_SPEECH",

"threshold": "BLOCK_MEDIUM_AND_ABOVE"

},

{

"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",

"threshold": "BLOCK_MEDIUM_AND_ABOVE"

},

{

"category": "HARM_CATEGORY_DANGEROUS_CONTENT",

"threshold": "BLOCK_MEDIUM_AND_ABOVE"

},

]

model = genai.GenerativeModel(model_name="gemini-1.0-pro-vision-latest",

generation_config=generation_config,

safety_settings=safety_settings)

# Validate that an image is present

if not (img := Path("image0.png")).exists():

raise FileNotFoundError(f"Could not find image: {img}")

image_parts = [

{

"mime_type": "image/png",

"data": Path("image0.png").read_bytes()

},

]

prompt_parts = [

"이미지의 물건을 다양한 용도를 제시해줘. 가장 기본적인 용도부터, 정말 이색적인 사용처도 제시해줘.",

image_parts[0],

]

response = model.generate_content(prompt_parts)

print(response.text)
