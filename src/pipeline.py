"""
Main Pipeline Module
Orchestrates all components to process medical conversations
"""

import json
import os
from typing import Dict
from datetime import datetime

from .preprocessing import preprocess_conversation
from .ner_extraction import extract_ner_from_conversation
from .keyword_extraction import extract_keywords_from_conversation
from .summarization import summarize_conversation
from .sentiment_intent import analyze_sentiment_intent
from .soap_generator import generate_soap_note


def run_pipeline(input_file_path: str, output_dir: str = "outputs") -> Dict:
    """
    Run the complete pipeline on a medical conversation file.
    
    Args:
        input_file_path: Path to raw conversation file
        output_dir: Directory to save outputs
        
    Returns:
        Dictionary with all extracted information
    """
    print(f"Starting pipeline for: {input_file_path}")
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Step 1: Preprocessing
    print("Step 1: Preprocessing conversation...")
    processed_data = preprocess_conversation(input_file_path)
    
    # Step 2: NER Extraction
    print("Step 2: Extracting medical entities...")
    ner_data = extract_ner_from_conversation(processed_data)
    
    # Step 3: Keyword Extraction
    print("Step 3: Extracting keywords...")
    keyword_data = extract_keywords_from_conversation(processed_data)
    
    # Step 4: Summarization
    print("Step 4: Generating medical summary...")
    summary_data = summarize_conversation(processed_data)
    
    # Step 5: Sentiment & Intent Analysis
    print("Step 5: Analyzing sentiment and intent...")
    sentiment_data = analyze_sentiment_intent(processed_data)
    
    # Step 6: Generate Structured Medical Report
    print("Step 6: Generating structured medical report...")
    medical_report = {
        "Patient_Name": extract_patient_name(processed_data.get("full_text", "")),
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Symptoms": ner_data.get("Symptoms", []),
        "Diagnosis": ner_data.get("Diagnosis", [""])[0] if ner_data.get("Diagnosis") else "Not specified",
        "Treatment": ner_data.get("Treatment", []),
        "Current_Status": summary_data.get("Medical_Summary", "")[:200],
        "Prognosis": ' '.join(ner_data.get("Prognosis", [])) if ner_data.get("Prognosis") else "Not specified"
    }
    
    # Step 7: Generate SOAP Note
    print("Step 7: Generating SOAP note...")
    soap_note = generate_soap_note(processed_data, ner_data, summary_data.get("Medical_Summary", ""))
    
    # Combine all results
    final_output = {
        "Medical_Report": medical_report,
        "NER_Extraction": ner_data,
        "Keywords": keyword_data,
        "Summary": summary_data,
        "Sentiment_Intent": sentiment_data,
        "SOAP_Note": soap_note
    }
    
    # Save outputs
    print("Saving outputs...")
    
    # Save medical summary
    with open(os.path.join(output_dir, "medical_summary.json"), 'w', encoding='utf-8') as f:
        json.dump(medical_report, f, indent=2, ensure_ascii=False)
    
    # Save sentiment and intent
    with open(os.path.join(output_dir, "sentiment_intent.json"), 'w', encoding='utf-8') as f:
        json.dump(sentiment_data, f, indent=2, ensure_ascii=False)
    
    # Save SOAP note
    with open(os.path.join(output_dir, "soap_note.json"), 'w', encoding='utf-8') as f:
        json.dump(soap_note, f, indent=2, ensure_ascii=False)
    
    # Save complete output
    with open(os.path.join(output_dir, "complete_output.json"), 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)
    
    print("Pipeline completed successfully!")
    print(f"Outputs saved to: {output_dir}/")
    
    return final_output


def extract_patient_name(text: str) -> str:
    """Extract patient name from text."""
    import re
    patterns = [
        r'Patient:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?),?\s+(?:how|feeling|doing)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    
    return "Patient"


if __name__ == "__main__":
    # Test the pipeline
    test_file = "data/raw_transcripts/sample_conversation.txt"
    if os.path.exists(test_file):
        result = run_pipeline(test_file)
        print("\n=== Pipeline Results ===")
        print(json.dumps(result, indent=2))
    else:
        print(f"Test file not found: {test_file}")


