import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_lawyers():
    with open("backend/agents/lawyers.json", "r") as f:
        return json.load(f)

def get_solutions(risky_clauses):
    solutions = []
    for clause in risky_clauses:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a legal advisor. Give simple practical solutions."
                },
                {
                    "role": "user",
                    "content": f"This clause is {clause['risk_level']} risk: {clause['clause']}. Give solution in 2-3 sentences."
                }
            ]
        )
        solution = response.choices[0].message.content
        lawyers = []
        if clause['risk_level'] == "High":
            lawyers = load_lawyers()
        solutions.append({
            "clause": clause['clause'],
            "risk_level": clause['risk_level'],
            "solution": solution,
            "lawyers": lawyers
        })
    return solutions