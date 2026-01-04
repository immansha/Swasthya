"""
Medical Named Entity Recognition Module
Extracts medical entities: Symptoms, Diagnosis, Treatment, Prognosis
"""

import json
import re
from typing import Dict, List, Set
import spacy
from spacy import displacy

# Try to load scispaCy model, fallback to regular spaCy if not available
try:
    nlp = spacy.load("en_ner_bc5cdr_md")
    SCISPACY_AVAILABLE = True
except OSError:
    try:
        nlp = spacy.load("en_core_web_sm")
        SCISPACY_AVAILABLE = False
        print("Warning: scispaCy model not found. Using en_core_web_sm instead.")
        print("For better medical NER, install: pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_ner_bc5cdr_md-0.5.4.tar.gz")
    except OSError:
        print("Error: No spaCy model found. Please install: python -m spacy download en_core_web_sm")
        nlp = None


# Medical keywords for entity classification
SYMPTOM_KEYWORDS = [
    'pain', 'ache', 'discomfort', 'sore', 'tender', 'stiff', 'numb',
    'tingling', 'headache', 'dizziness', 'nausea', 'vomiting', 'fever',
    'fatigue', 'weakness', 'swelling', 'inflammation', 'rash', 'itch'
]

DIAGNOSIS_KEYWORDS = [
    'diagnosis', 'diagnosed', 'condition', 'disease', 'disorder', 'syndrome',
    'injury', 'fracture', 'infection', 'inflammation', 'chronic', 'acute'
]

TREATMENT_KEYWORDS = [
    'treatment', 'therapy', 'medication', 'medicine', 'drug', 'prescription',
    'physiotherapy', 'surgery', 'operation', 'procedure', 'exercise',
    'painkiller', 'antibiotic', 'dose', 'session', 'appointment'
]

PROGNOSIS_KEYWORDS = [
    'recovery', 'prognosis', 'outcome', 'heal', 'improve', 'better',
    'recover', 'expected', 'timeline', 'months', 'weeks', 'days'
]


def extract_medical_entities(text: str) -> Dict[str, List[str]]:
    """
    Extract medical entities from text using spaCy/scispaCy and keyword matching.
    
    Args:
        text: Input medical text
        
    Returns:
        Dictionary with extracted entities by category
    """
    if nlp is None:
        return {
            "Symptoms": [],
            "Diagnosis": [],
            "Treatment": [],
            "Prognosis": []
        }
    
    doc = nlp(text)
    
    # Extract entities using NER
    entities = {}
    for ent in doc.ents:
        label = ent.label_
        text_ent = ent.text.lower()
        
        # Classify entities based on labels and keywords
        if any(keyword in text_ent for keyword in SYMPTOM_KEYWORDS):
            if "Symptoms" not in entities:
                entities["Symptoms"] = []
            if ent.text not in entities["Symptoms"]:
                entities["Symptoms"].append(ent.text)
        elif any(keyword in text_ent for keyword in DIAGNOSIS_KEYWORDS):
            if "Diagnosis" not in entities:
                entities["Diagnosis"] = []
            if ent.text not in entities["Diagnosis"]:
                entities["Diagnosis"].append(ent.text)
        elif any(keyword in text_ent for keyword in TREATMENT_KEYWORDS):
            if "Treatment" not in entities:
                entities["Treatment"] = []
            if ent.text not in entities["Treatment"]:
                entities["Treatment"].append(ent.text)
        elif any(keyword in text_ent for keyword in PROGNOSIS_KEYWORDS):
            if "Prognosis" not in entities:
                entities["Prognosis"] = []
            if ent.text not in entities["Prognosis"]:
                entities["Prognosis"].append(ent.text)
    
    # Additional keyword-based extraction for better coverage
    symptoms = extract_by_keywords(text, SYMPTOM_KEYWORDS)
    diagnosis = extract_by_keywords(text, DIAGNOSIS_KEYWORDS)
    treatment = extract_by_keywords(text, TREATMENT_KEYWORDS)
    prognosis = extract_by_keywords(text, PROGNOSIS_KEYWORDS)
    
    # Combine NER and keyword-based results
    result = {
        "Symptoms": list(set(entities.get("Symptoms", []) + symptoms)),
        "Diagnosis": list(set(entities.get("Diagnosis", []) + diagnosis)),
        "Treatment": list(set(entities.get("Treatment", []) + treatment)),
        "Prognosis": list(set(entities.get("Prognosis", []) + prognosis))
    }
    
    # Clean and deduplicate
    for key in result:
        result[key] = [item.strip() for item in result[key] if item.strip()]
        result[key] = list(dict.fromkeys(result[key]))  # Preserve order, remove duplicates
    
    return result


def extract_by_keywords(text: str, keywords: List[str]) -> List[str]:
    """Extract phrases containing medical keywords."""
    found_phrases = []
    text_lower = text.lower()
    
    for keyword in keywords:
        # Find sentences or phrases containing the keyword
        pattern = rf'[^.]*{re.escape(keyword)}[^.]*\.?'
        matches = re.findall(pattern, text, re.IGNORECASE)
        
        for match in matches:
            # Extract noun phrases or meaningful chunks
            cleaned = match.strip()
            if len(cleaned) > 10 and len(cleaned) < 200:  # Reasonable length
                found_phrases.append(cleaned)
    
    return found_phrases[:10]  # Limit to top 10


def extract_ner_from_conversation(processed_data: Dict[str, str]) -> Dict[str, List[str]]:
    """
    Extract NER from processed conversation data.
    
    Args:
        processed_data: Dictionary with 'doctor_text', 'patient_text', 'full_text'
        
    Returns:
        Dictionary with extracted medical entities
    """
    # Use full text for comprehensive extraction
    full_text = processed_data.get("full_text", "")
    
    # Extract entities
    entities = extract_medical_entities(full_text)
    
    return entities


if __name__ == "__main__":
    # Test NER extraction
    test_text = "Patient experienced neck pain and back pain after a car accident. Diagnosed with whiplash injury. Treatment includes physiotherapy and painkillers. Full recovery expected in six months."
    result = extract_medical_entities(test_text)
    print(json.dumps(result, indent=2))

