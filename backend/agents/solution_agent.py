import json
import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def load_lawyers():
    lawyers_path = os.path.join(os.path.dirname(__file__), 'lawyers.json')
    with open(lawyers_path, 'r') as f:
        return json.load(f)

def get_solutions(risky_clauses):
    solutions = []
    for clause in risky_clauses:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": f"This clause is {clause['risk_level']} risk: {clause['clause']}. Give a simple practical solution in 2-3 sentences."}]
        )
        lawyers = []
        if clause['risk_level'] == "High":
            lawyers = load_lawyers()
        solutions.append({
            "clause": clause['clause'],
            "risk_level": clause['risk_level'],
            "solution": response.choices[0].message.content,
            "lawyers": lawyers
        })
    return solutions