import streamlit as st
from PIL import Image
import base64
from io import BytesIO
from gigachat import GigaChat

st.set_page_config(page_title="ЖруСчиталка", page_icon="🍖", layout="centered")

st.title("🔥 ЖруСчиталка")
st.subheader("Считаем, сколько ты сегодня НАЖРАЛ по фото")

credentials = st.secrets.get("GIGACHAT_CREDENTIALS")
if not credentials:
    st.error("❌ Ключ не найден. Проверь Secrets → GIGACHAT_CREDENTIALS")
    st.stop()

model = GigaChat(credentials=credentials, verify_ssl_certs=False, model="GigaChat-Max")

uploaded_file = st.file_uploader("📸 Загрузи фото своей тарелки", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Ого, ну ты и подготовился 👀", use_column_width=True)
    
    if st.button("🔥 Посчитать, сколько я сегодня сожрал!", type="primary", use_container_width=True):
        with st.spinner("ЖруСчиталка жрёт глазами твою тарелку... 🤤"):
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()

            # ← ИСПРАВЛЕННЫЙ ФОРМАТ ДЛЯ GIGACHAT VISION
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Ты дерзкий и вредный эксперт по питанию. Посмотри на фото еды и скажи максимально честно и с юмором:\n1. Что именно человек собрался сожрать\n2. Примерные порции в граммах\n3. Калории + БЖУ\n4. Добавь комментарий в стиле 'ну ты и обжора', 'это вообще можно есть?' или 'диета сегодня умерла'"
                        },
                        {
                            "type": "image",
                            "image": img_base64          # ← только base64, без data:
                        }
                    ]
                }
            ]
            
            response = model.chat(messages)
            st.success("Вот что ты там намешал:")
            st.markdown(response.choices[0].message.content)

st.caption("ЖруСчиталка © 2026 • Работает на GigaChat")
