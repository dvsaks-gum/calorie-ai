import streamlit as st
from PIL import Image
import base64
from io import BytesIO
import requests

st.set_page_config(page_title="ЖруСчиталка", page_icon="🍖", layout="centered")

st.title("🔥 ЖруСчиталка")
st.subheader("Считаем, сколько ты сегодня НАЖРАЛ по фото")

credentials = st.secrets.get("GIGACHAT_CREDENTIALS")
if not credentials:
    st.error("❌ Ключ не найден. Проверь Secrets → GIGACHAT_CREDENTIALS")
    st.stop()

uploaded_file = st.file_uploader("📸 Загрузи фото своей тарелки", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Ого, ну ты и подготовился 👀", use_column_width=True)
    
    if st.button("🔥 Посчитать, сколько я сегодня сожрал!", type="primary", use_container_width=True):
        with st.spinner("ЖруСчиталка анализирует твою тарелку... 🤤"):
            
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()

            # 1. Получаем токен
            token_url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
            token_headers = {
                "Authorization": f"Basic {credentials}",
                "Content-Type": "application/x-www-form-urlencoded",
                "RqUID": "1"
            }
            token_data = {"scope": "GIGACHAT_API_PERS"}

            token_response = requests.post(token_url, headers=token_headers, data=token_data, verify=False, timeout=10)

            if token_response.status_code != 200:
                st.error(f"Ошибка получения токена: {token_response.status_code}")
                st.stop()

            access_token = token_response.json().get("access_token")

            # 2. Отправляем фото на анализ
            chat_url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "GigaChat-Max",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Ты дерзкий и вредный эксперт по питанию. Посмотри на фото еды и ответь максимально честно и с юмором:\n1. Что именно человек собрался сожрать\n2. Примерные порции в граммах\n3. Калории + БЖУ\n4. Добавь едкий комментарий в стиле 'ну ты и обжора' или 'диета сегодня умерла'"
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}
                            }
                        ]
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 900
            }

            response = requests.post(chat_url, headers=headers, json=payload, verify=False, timeout=30)

            if response.status_code == 200:
                result = response.json()
                st.success("Готово! Вот что ты там намешал:")
                st.markdown(result["choices"][0]["message"]["content"])
            else:
                st.error(f"Ошибка анализа: {response.status_code}\n{response.text[:400]}")

st.caption("ЖруСчиталка © 2026 • Работает на GigaChat")
