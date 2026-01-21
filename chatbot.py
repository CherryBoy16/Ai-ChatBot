from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_response(user_input, file_text=""):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful AI chatbot. "
                "If file content is provided, answer strictly based on it. "
                "If the answer is not in the file, say you don't know."
            )
        }
    ]

    # Add file context only if user uploaded something
    if file_text:
        messages.append({
            "role": "system",
            "content": f"File Content:\n{file_text[:12000]}"
        })

    messages.append({
        "role": "user",
        "content": user_input
    })

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.3
    )

    return response.choices[0].message.content
