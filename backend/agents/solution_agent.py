import json
import os
from openai import OpenAI

# OpenAI client setup
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load lawyers from JSON file
def load_lawyers():
    with open("backend/agents/lawyers.json", "r") as f:
        return json.load(f)

# Generate solution for each risky clause
def get_solutions(risky_clauses):
    solutions = []
    
    for clause in risky_clauses:
        # Ask AI for solution
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a legal advisor. Give practical simple solutions for risky legal clauses."
                },
                {
                    "role": "user",
                    "content": f"This clause is {clause['risk_level']} risk: {clause['clause']}. Give a simple practical solution in 2-3 sentences."
                }
            ]
        )
        
        solution = response.choices[0].message.content
        
        # If High risk, suggest lawyers too
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