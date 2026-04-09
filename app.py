import streamlit as st
from PIL import Image
import google.generativeai as genai
import os

st.set_page_config(page_title="Калькулятор калорий ИИ", page_icon="🍽️")
st.title("🍽️ ИИ-калькулятор калорий по фото")

api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Нет API-ключа! Добавь в Secrets Streamlit.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

uploaded_file = st.file_uploader("Загрузи фото еды", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Твоя еда", use_column_width=True)
    
    if st.button("🔥 Посчитать калории"):
        with st.spinner("ИИ думает..."):
            prompt = """Ты эксперт по питанию. Проанализируй фото еды:
            1. Перечисли все продукты
            2. Оцени примерные порции
            3. Посчитай калории и БЖУ (белки, жиры, углеводы)
            4. Выведи красиво и понятно"""
            
            response = model.generate_content([prompt, image])
            st.success("Готово!")
            st.markdown(response.text)
