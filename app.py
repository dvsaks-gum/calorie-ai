import streamlit as st
from PIL import Image
import base64
from io import BytesIO
from openai import OpenAI

st.set_page_config(page_title="Калькулятор калорий Grok", page_icon="🍽️")
st.title("🍽️ Grok ИИ-калькулятор калорий по фото")

# Ключ из Secrets
api_key = st.secrets.get("GROK_API_KEY")
if not api_key:
    st.error("❌ Нет Grok API ключа! Добавь в Secrets → GROK_API_KEY")
    st.stop()

client = OpenAI(
    api_key=api_key,
    base_url="https://api.x.ai/v1"
)

uploaded_file = st.file_uploader("Загрузи фото еды", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Твоя еда", use_column_width=True)
    
    if st.button("🔥 Посчитать калории с Grok"):
        with st.spinner("Grok думает..."):
            # Конвертируем фото в base64
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()

            response = client.chat.completions.create(
                model="grok-4.20-reasoning",   # самая новая модель с vision
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Ты эксперт по питанию. Проанализируй фото еды:\n"
                                        "1. Перечисли все продукты\n"
                                        "2. Оцени примерные порции в граммах\n"
                                        "3. Посчитай калории и БЖУ (белки, жиры, углеводы)\n"
                                        "4. Выведи результат красиво и понятно"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{img_base64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=800
            )
            
            st.success("✅ Готово!")
            st.markdown(response.choices[0].message.content)
