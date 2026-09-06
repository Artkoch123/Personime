from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze(text):
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "Ты определяешь аниме-персонажа по описанию человека. Отвечай строго в формате JSON: {\"character\": \"имя\", \"anime\": \"название\", \"explanation\": \"почему\"}"},
            {"role": "user", "content": text}
        ],
        response_format={"type": "json_object"}
    )
    return response.choices[0].message.content