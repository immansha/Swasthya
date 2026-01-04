"""
SOAP Note Generator Module
Converts medical conversation into structured SOAP clinical notes
"""

import json
import re
from typing import Dict, List
from datetime import datetime


def extract_patient_name(text: str) -> str:
    """Extract patient name from conversation."""
    # Look for patterns like "Janet" or "Patient: [Name]"
    patterns = [
        r'Patient:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?),?\s+(?:how|feeling|doing)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    
    return "Patient"


def generate_soap_note(
    processed_data: Dict[str, str],
    ner_data: Dict[str, List[str]],
    summary: str
) -> Dict[str, any]:
    """
    Generate SOAP note from conversation data.
    
    Args:
        processed_data: Processed conversation text
        ner_data: Extracted medical entities
        summary: Medical summary
        
    Returns:
        Structured SOAP note
    """
    patient_text = processed_data.get("patient_text", "")
    doctor_text = processed_data.get("doctor_text", "")
    full_text = processed_data.get("full_text", "")
    
    # Extract patient name
    patient_name = extract_patient_name(full_text)
    
    # SUBJECTIVE: Patient's reported symptoms and concerns
    subjective = {
        "Chief_Complaint": extract_chief_complaint(patient_text),
        "History_of_Present_Illness": extract_hpi(patient_text, ner_data),
        "Patient_Reported_Symptoms": ner_data.get("Symptoms", []),
        "Patient_Concerns": extract_concerns(patient_text)
    }
    
    # OBJECTIVE: Clinical observations and findings
    objective = {
        "Physical_Examination": extract_examination_findings(doctor_text),
        "Clinical_Observations": extract_observations(doctor_text),
        "Diagnostic_Information": extract_diagnostic_info(full_text)
    }
    
    # ASSESSMENT: Diagnosis and clinical assessment
    assessment = {
        "Primary_Diagnosis": ner_data.get("Diagnosis", ["Not specified"])[0] if ner_data.get("Diagnosis") else "Not specified",
        "Differential_Diagnosis": ner_data.get("Diagnosis", []),
        "Clinical_Assessment": summary
    }
    
    # PLAN: Treatment plan and follow-up
    plan = {
        "Treatment_Plan": ner_data.get("Treatment", []),
        "Medications": extract_medications(full_text),
        "Therapy_Recommendations": extract_therapy(full_text),
        "Follow_Up": extract_followup(doctor_text),
        "Prognosis": ' '.join(ner_data.get("Prognosis", [])) if ner_data.get("Prognosis") else "Not specified"
    }
    
    soap_note = {
        "Patient_Name": patient_name,
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Subjective": subjective,
        "Objective": objective,
        "Assessment": assessment,
        "Plan": plan
    }
    
    return soap_note


def extract_chief_complaint(patient_text: str) -> str:
    """Extract chief complaint from patient text."""
    # Look for first significant symptom mention
    sentences = re.split(r'[.!?]+', patient_text)
    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in ['pain', 'ache', 'discomfort', 'problem', 'issue']):
            return sentence.strip()[:200]  # Limit length
    return "Not specified"


def extract_hpi(patient_text: str, ner_data: Dict) -> str:
    """Extract History of Present Illness."""
    # Combine symptoms and timeline information
    symptoms = ', '.join(ner_data.get("Symptoms", []))
    if symptoms:
        return f"Patient reports: {symptoms}"
    return "See patient text for details"


def extract_concerns(patient_text: str) -> List[str]:
    """Extract patient concerns."""
    concerns = []
    concern_keywords = ['worried', 'concerned', 'afraid', 'uncertain', 'question']
    
    sentences = re.split(r'[.!?]+', patient_text)
    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in concern_keywords):
            concerns.append(sentence.strip())
    
    return concerns[:5]  # Limit to 5 concerns


def extract_examination_findings(doctor_text: str) -> str:
    """Extract physical examination findings."""
    exam_keywords = ['examination', 'exam', 'observed', 'found', 'noted', 'appears']
    
    sentences = re.split(r'[.!?]+', doctor_text)
    exam_sentences = [
        s.strip() for s in sentences
        if any(keyword in s.lower() for keyword in exam_keywords)
    ]
    
    if exam_sentences:
        return '. '.join(exam_sentences[:3])
    return "No specific examination findings documented"


def extract_observations(doctor_text: str) -> List[str]:
    """Extract clinical observations."""
    observations = []
    observation_keywords = ['progress', 'improving', 'healing', 'better', 'recovery']
    
    sentences = re.split(r'[.!?]+', doctor_text)
    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in observation_keywords):
            observations.append(sentence.strip())
    
    return observations[:5]


def extract_diagnostic_info(text: str) -> List[str]:
    """Extract diagnostic information."""
    diagnostic_info = []
    diagnostic_keywords = ['diagnosed', 'diagnosis', 'test', 'result', 'finding']
    
    sentences = re.split(r'[.!?]+', text)
    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in diagnostic_keywords):
            diagnostic_info.append(sentence.strip())
    
    return diagnostic_info[:5]


def extract_medications(text: str) -> List[str]:
    """Extract medications mentioned."""
    medications = []
    medication_keywords = ['medication', 'medicine', 'drug', 'painkiller', 'prescription', 'pill']
    
    sentences = re.split(r'[.!?]+', text)
    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in medication_keywords):
            # Try to extract medication name
            medication_match = re.search(r'(\w+(?:\s+\w+)?)\s+(?:medication|medicine|drug|painkiller)', sentence, re.IGNORECASE)
            if medication_match:
                medications.append(medication_match.group(1))
            else:
                medications.append(sentence.strip()[:100])
    
    return list(set(medications))[:10]


def extract_therapy(text: str) -> List[str]:
    """Extract therapy recommendations."""
    therapy = []
    therapy_keywords = ['physiotherapy', 'therapy', 'exercise', 'session', 'treatment']
    
    sentences = re.split(r'[.!?]+', text)
    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in therapy_keywords):
            therapy.append(sentence.strip()[:150])
    
    return therapy[:5]


def extract_followup(doctor_text: str) -> str:
    """Extract follow-up information."""
    followup_keywords = ['follow-up', 'follow up', 'appointment', 'schedule', 'next visit']
    
    sentences = re.split(r'[.!?]+', doctor_text)
    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in followup_keywords):
            return sentence.strip()
    
    return "Follow-up as needed"


if __name__ == "__main__":
    # Test SOAP generation
    test_processed = {
        "patient_text": "I'm doing much better. The neck pain has reduced. Still some back discomfort.",
        "doctor_text": "Patient shows good progress. Continue physiotherapy.",
        "full_text": "Patient doing better. Neck pain reduced. Continue therapy."
    }
    test_ner = {
        "Symptoms": ["neck pain", "back discomfort"],
        "Diagnosis": ["whiplash injury"],
        "Treatment": ["physiotherapy"],
        "Prognosis": ["full recovery in six months"]
    }
    test_summary = "Patient recovering from whiplash injury with improving symptoms."
    
    result = generate_soap_note(test_processed, test_ner, test_summary)
    print(json.dumps(result, indent=2))


