import streamlit as st
from pathlib import Path
import google.generativeai as genai
import tempfile

# Google Generative AI 설정
genai.configure(api_key="AIzaSyBz3OcS81G4GEpCQvVWMbuxENBPnC9EGco")
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]
model = genai.GenerativeModel(model_name="gemini-1.0-pro-vision-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Streamlit 앱 설정
st.title("이미지 용도 제안 서비스")

uploaded_file = st.file_uploader("이미지 업로드", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        uploaded_image_path = Path(tmp_file.name)

    st.image(uploaded_image_path, caption="업로드된 이미지", use_column_width=True)

    if st.button("이미지 용도 제안"):
        image_parts = [{"mime_type": "image/png", "data": uploaded_image_path.read_bytes()}]
        prompt_parts = ["이미지의 물건을 다양한 용도를 제시해줘. 가장 기본적인 용도부터, 정말 이색적인 사용처도 제시해줘\n\n", image_parts[0], "\n\n"]
        response = model.generate_content(prompt_parts)
        st.write(response.text)
