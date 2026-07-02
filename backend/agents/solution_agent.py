import os
import requests
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def find_nearby_lawyers(location):
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"property lawyer near {location}",
        "key": api_key
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    lawyers = []
    for place in data["results"][:5]:
        lawyers.append({
            "name": place["name"],
            "address": place["formatted_address"],
            "rating": place.get("rating", "N/A"),
        })
    return lawyers

def get_solutions(risky_clauses, user_location="Kerala"):
    solutions = []
    
    for clause in risky_clauses:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a legal advisor. Give practical simple solutions."
                },
                {
                    "role": "user",
                    "content": f"This clause is {clause['risk_level']} risk: {clause['clause']}. Give solution in 2-3 sentences."
                }
            ]
        )
        
        solution = response.choices[0].message.content
        
        # If High risk, search nearby lawyers
        lawyers = []
        if clause['risk_level'] == "High":
            lawyers = find_nearby_lawyers(user_location)
        
        solutions.append({
            "clause": clause['clause'],
            "risk_level": clause['risk_level'],
            "solution": solution,
            "lawyers": lawyers
        })
    
    return solutions