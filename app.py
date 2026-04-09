import streamlit as st
from PIL import Image
import base64
from io import BytesIO
from openai import OpenAI

st.set_page_config(
    page_title="ЖруСчиталка",
    page_icon="🍖",
    layout="centered"
)

st.title("🔥 ЖруСчиталка")
st.subheader("Считаем, сколько ты сегодня НАЖРАЛ по фото")

# Ключ
api_key = st.secrets.get("GROK_API_KEY")
if not api_key:
    st.error("❌ Ключ не найден. Проверь Secrets → GROK_API_KEY")
    st.stop()

client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")

uploaded_file = st.file_uploader("📸 Загрузи фото своей тарелки", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Ого, ну ты и подготовился 👀", use_column_width=True)
    
    if st.button("🔥 Посчитать, сколько я сегодня сожрал!", type="primary", use_container_width=True):
        with st.spinner("ЖруСчиталка внимательно жрёт глазами твою тарелку... 🤤"):
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()

            response = client.chat.completions.create(
                model="grok-vision-beta",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Ты дерзкий и немного вредный эксперт по питанию. Посмотри на фото еды и скажи максимально честно и с юмором:\n1. Что именно человек собрался сожрать\n2. Примерные порции в граммах\n3. Сколько там калорий и БЖУ\n4. Добавь едкий комментарий в стиле 'ну ты и обжора', 'это вообще можно есть?' или 'диета умерла сегодня'"},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
                        ]
                    }
                ],
                max_tokens=900
            )
            
            st.success("Вот что ты там намешал:")
            st.markdown(response.choices[0].message.content)

st.caption("ЖруСчиталка © 2026 • Считает калории, пока ты не лопнул")
