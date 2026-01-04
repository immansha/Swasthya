"""
Text Preprocessing Module
Handles cleaning, normalization, and segmentation of medical conversations
"""

import re
import json
from typing import Dict, List


def remove_speaker_tags(text: str) -> str:
    """Remove speaker tags like 'Doctor:' and 'Patient:' from text."""
    # Remove speaker tags at the beginning of lines
    text = re.sub(r'^(Doctor|Patient):\s*', '', text, flags=re.MULTILINE)
    return text.strip()


def normalize_text(text: str) -> str:
    """Normalize text by removing extra whitespace and fixing common issues."""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove multiple periods
    text = re.sub(r'\.{2,}', '.', text)
    return text.strip()


def segment_conversation(text: str) -> Dict[str, str]:
    """
    Segment conversation into doctor and patient text.
    
    Args:
        text: Raw conversation text with speaker tags
        
    Returns:
        Dictionary with 'doctor_text', 'patient_text', and 'full_text'
    """
    doctor_lines = []
    patient_lines = []
    all_lines = []
    
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('Doctor:'):
            doctor_text = line.replace('Doctor:', '').strip()
            doctor_lines.append(doctor_text)
            all_lines.append(doctor_text)
        elif line.startswith('Patient:'):
            patient_text = line.replace('Patient:', '').strip()
            patient_lines.append(patient_text)
            all_lines.append(patient_text)
        else:
            # If no tag, assume continuation of previous speaker
            if doctor_lines and len(doctor_lines) > len(patient_lines):
                doctor_lines[-1] += ' ' + line
            elif patient_lines:
                patient_lines[-1] += ' ' + line
            all_lines.append(line)
    
    doctor_text = ' '.join(doctor_lines)
    patient_text = ' '.join(patient_lines)
    full_text = ' '.join(all_lines)
    
    # Normalize all texts
    doctor_text = normalize_text(doctor_text)
    patient_text = normalize_text(patient_text)
    full_text = normalize_text(full_text)
    
    return {
        "doctor_text": doctor_text,
        "patient_text": patient_text,
        "full_text": full_text
    }


def preprocess_conversation(file_path: str) -> Dict[str, str]:
    """
    Main preprocessing function that reads a conversation file and processes it.
    
    Args:
        file_path: Path to the raw conversation file
        
    Returns:
        Dictionary with processed text segments
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_text = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Conversation file not found: {file_path}")
    
    # Segment the conversation
    segmented = segment_conversation(raw_text)
    
    # Save processed data
    output_path = file_path.replace('raw_transcripts', 'processed').replace('.txt', '.json')
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(segmented, f, indent=2, ensure_ascii=False)
    
    return segmented


if __name__ == "__main__":
    # Test the preprocessing
    test_path = "data/raw_transcripts/sample_conversation.txt"
    result = preprocess_conversation(test_path)
    print(json.dumps(result, indent=2))


