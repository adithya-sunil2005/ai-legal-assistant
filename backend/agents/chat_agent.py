import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def answer_question(question, document_text):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": f"Document: {document_text}\n\nQuestion: {question}\n\nAnswer in simple plain language."}]
    )
    return {
        "question": question,
        "answer": response.choices[0].message.content
    }