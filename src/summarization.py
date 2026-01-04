"""
Medical Text Summarization Module
Generates concise summaries of medical conversations using BART
"""

import json
from typing import Dict

try:
    from transformers import pipeline, BartForConditionalGeneration, BartTokenizer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("Warning: Transformers not available. Using simple extractive summarization.")


def summarize_with_bart(text: str, max_length: int = 150, min_length: int = 50) -> str:
    """
    Summarize text using BART model.
    
    Args:
        text: Input text to summarize
        max_length: Maximum length of summary
        min_length: Minimum length of summary
        
    Returns:
        Summarized text
    """
    if not TRANSFORMERS_AVAILABLE:
        return summarize_simple(text)
    
    try:
        # Use facebook/bart-large-cnn for summarization
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        
        # Handle long texts by chunking
        if len(text) > 1024:
            # Split into chunks and summarize each
            chunks = [text[i:i+1024] for i in range(0, len(text), 1024)]
            summaries = []
            for chunk in chunks:
                summary = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
                summaries.append(summary[0]['summary_text'])
            return ' '.join(summaries)
        else:
            summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
            return summary[0]['summary_text']
    except Exception as e:
        print(f"BART summarization failed: {e}")
        print("Falling back to simple summarization...")
        return summarize_simple(text)


def summarize_simple(text: str, num_sentences: int = 3) -> str:
    """
    Simple extractive summarization by selecting key sentences.
    
    Args:
        text: Input text
        num_sentences: Number of sentences to include
        
    Returns:
        Summary text
    """
    import re
    
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    if len(sentences) <= num_sentences:
        return '. '.join(sentences) + '.'
    
    # Score sentences (simple heuristic: longer sentences with medical keywords)
    medical_keywords = ['patient', 'diagnosis', 'treatment', 'symptom', 'pain', 'injury', 
                       'recovery', 'therapy', 'medication', 'doctor', 'condition']
    
    scored_sentences = []
    for i, sentence in enumerate(sentences):
        score = len(sentence)
        # Boost score for medical keywords
        for keyword in medical_keywords:
            if keyword.lower() in sentence.lower():
                score += 20
        # Boost first and last sentences
        if i == 0 or i == len(sentences) - 1:
            score += 10
        
        scored_sentences.append((score, sentence))
    
    # Sort by score and take top N
    scored_sentences.sort(reverse=True, key=lambda x: x[0])
    top_sentences = [s[1] for s in scored_sentences[:num_sentences]]
    
    # Sort back to original order
    top_sentences = [s for s in sentences if s in top_sentences]
    
    return '. '.join(top_sentences) + '.'


def summarize_conversation(processed_data: Dict[str, str]) -> Dict[str, str]:
    """
    Summarize medical conversation.
    
    Args:
        processed_data: Dictionary with processed text
        
    Returns:
        Dictionary with medical summary
    """
    full_text = processed_data.get("full_text", "")
    
    # Generate summary
    summary = summarize_with_bart(full_text, max_length=200, min_length=80)
    
    return {
        "Medical_Summary": summary
    }


if __name__ == "__main__":
    # Test summarization
    test_text = """
    Patient experienced neck pain and back pain after a car accident three weeks ago. 
    Diagnosed with whiplash injury. Treatment includes 10 physiotherapy sessions and painkillers. 
    Patient has completed 8 sessions and reports significant improvement. 
    Neck pain has reduced, but some back discomfort remains. 
    Doctor expects full recovery within six months with continued therapy.
    """
    result = summarize_conversation({"full_text": test_text})
    print(json.dumps(result, indent=2))


