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
        with st.spinner("ЖруСчиталка жрёт глазами твою тарелку... 🤤"):
            
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()

            # === 1. Получаем access token ===
            token_url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
            headers_token = {
                "Authorization": f"Basic {credentials}",
                "Content-Type": "application/x-www-form-urlencoded",
                "RqUID": "1"
            }
            data_token = {"scope": "GIGACHAT_API_PERS"}

            token_response = requests.post(token_url, headers=headers_token, data=data_token, verify=False, timeout=10)

            st.write(f"**Статус токена:** {token_response.status_code}")   # ← отладка
            st.write(f"**Ответ сервера:** {token_response.text[:500]}...") # ← отладка

            try:
                access_token = token_response.json().get("access_token")
            except Exception as e:
                st.error(f"Не удалось получить токен. Ошибка: {e}")
                st.stop()

            # === 2. Отправляем фото ===
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
                            {"type": "text", "text": "Ты дерзкий и вредный эксперт по питанию... (твой промпт)"},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
                        ]
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 900
            }

            response = requests.post(chat_url, headers=headers, json=payload, verify=False)
            
            if response.status_code == 200:
                result = response.json()
                st.success("Вот что ты там намешал:")
                st.markdown(result["choices"][0]["message"]["content"])
            else:
                st.error(f"Ошибка чата: {response.status_code}\n{response.text}")

st.caption("ЖруСчиталка © 2026 • Работает напрямую через API Сбера")
