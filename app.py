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

st.info(f"Длина ключа: {len(credentials)} символов")  # отладка

uploaded_file = st.file_uploader("📸 Загрузи фото своей тарелки", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Ого, ну ты и подготовился 👀", use_column_width=True)
    
    if st.button("🔥 Посчитать, сколько я сегодня сожрал!", type="primary", use_container_width=True):
        with st.spinner("Получаем доступ к ЖруСчиталке..."):
            
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()

            # Запрос токена
            token_url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
            headers_token = {
                "Authorization": f"Basic {credentials}",
                "Content-Type": "application/x-www-form-urlencoded",
                "RqUID": "123e4567-e89b-12d3-a456-426614174000"
            }
            data_token = {"scope": "GIGACHAT_API_PERS"}

            token_response = requests.post(token_url, headers=headers_token, data=data_token, verify=False, timeout=15)

            st.write(f"**Статус токена:** {token_response.status_code}")
            st.write(f"**Ответ сервера:** {token_response.text}")

            if token_response.status_code != 200:
                st.error("Не удалось получить токен. Смотри выше ответ сервера.")
                st.stop()

            access_token = token_response.json().get("access_token")

            # Дальше идёт запрос к чату (пока не доходим)
            st.success("Токен получен! Сейчас будет анализ фото...")
            # (дальше можно добавить код чата, но сейчас главное — увидеть ошибку токена)

st.caption("ЖруСчиталка © 2026 • Отладочная версия")
