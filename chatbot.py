from groq import Groq
import os

# Set Groq API key securely (hardcoded for now, consider using environment variables for production)
client = Groq(api_key="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")

def ask_question(question, context):
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": "You are a smart AI tutor helping students understand their study material."
                },
                {
                    "role": "user",
                    "content": f"Here is the content:\n{context}\n\nNow answer this question:\n{question}"
                }
            ],
            temperature=0.2
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error occurred: {str(e)}"
