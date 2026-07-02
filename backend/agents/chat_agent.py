import os
from openai import OpenAI

# OpenAI client setup
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Answer user questions about the document
def answer_question(question, document_text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a legal assistant. Answer questions based only on the provided document. Give simple, clear answers."
            },
            {
                "role": "user",
                "content": f"Document: {document_text}\n\nQuestion: {question}\n\nAnswer in simple plain language."
            }
        ]
    )
    
    return {
        "question": question,
        "answer": response.choices[0].message.content
    }