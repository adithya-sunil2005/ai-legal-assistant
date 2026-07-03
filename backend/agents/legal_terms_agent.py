import json
import os

def flag_risky_clauses(text):
    # Load risk terms
    risk_terms_path = os.path.join(os.path.dirname(__file__), '..', 'risk_terms.json')
    with open(risk_terms_path, 'r') as f:
        risk_terms = json.load(f)
    
    risky_clauses = []
    text_lower = text.lower()
    
    # Check high risk terms
    for term in risk_terms["high"]:
        if term.lower() in text_lower:
            risky_clauses.append({
                "clause": term,
                "risk_level": "High"
            })
    
    # Check medium risk terms
    for term in risk_terms["medium"]:
        if term.lower() in text_lower:
            risky_clauses.append({
                "clause": term,
                "risk_level": "Medium"
            })
    
    # Check low risk terms
    for term in risk_terms["low"]:
        if term.lower() in text_lower:
            risky_clauses.append({
                "clause": term,
                "risk_level": "Low"
            })
    
    return risky_clauses