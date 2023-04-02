import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def send_chat(language: str, text: str):
    message = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": f"You are a {language} chat assistant. You should chat with me and not exceed 50 words per conversation"},
                {"role": "user", "content": text},
            ]
    )
    return message

if __name__ == '__main__':
    print(send_chat("hello who are you?"))