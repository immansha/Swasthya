"""
Sentiment and Intent Analysis Module
Analyzes patient sentiment and intent from conversation
"""

import json
import re
from typing import Dict, List

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("Warning: Transformers not available. Using rule-based sentiment analysis.")


# Sentiment categories
SENTIMENT_CATEGORIES = ["Anxious", "Neutral", "Reassured"]

# Intent categories
INTENT_CATEGORIES = [
    "Reporting symptoms",
    "Seeking reassurance",
    "Confirming recovery",
    "Asking questions",
    "Describing condition"
]

# Keywords for sentiment classification
ANXIOUS_KEYWORDS = [
    'worried', 'concerned', 'anxious', 'nervous', 'afraid', 'fear', 'scared',
    'uncertain', 'doubt', 'apprehensive', 'stress', 'panic'
]

REASSURED_KEYWORDS = [
    'better', 'improved', 'reassuring', 'confident', 'relieved', 'grateful',
    'thankful', 'appreciate', 'hopeful', 'optimistic', 'positive', 'good news'
]

# Keywords for intent classification
SYMPTOM_REPORTING_KEYWORDS = [
    'pain', 'ache', 'discomfort', 'feeling', 'experiencing', 'symptom',
    'problem', 'issue', 'bothering', 'hurting'
]

REASSURANCE_SEEKING_KEYWORDS = [
    'worried', 'concerned', 'should i', 'is it normal', 'what if', 'afraid',
    'wondering', 'question', 'doubt'
]

RECOVERY_CONFIRMING_KEYWORDS = [
    'better', 'improved', 'recovering', 'healing', 'progress', 'feeling good',
    'much better', 'doing well', 'getting better'
]


def analyze_sentiment_transformers(text: str) -> str:
    """Analyze sentiment using transformer model."""
    if not TRANSFORMERS_AVAILABLE:
        return analyze_sentiment_rule_based(text)
    
    try:
        # Use distilbert for sentiment analysis
        sentiment_analyzer = pipeline("sentiment-analysis", 
                                      model="distilbert-base-uncased-finetuned-sst-2-english")
        
        result = sentiment_analyzer(text[:512])  # Limit length
        label = result[0]['label']
        score = result[0]['score']
        
        # Map to our categories
        if label == 'POSITIVE' and score > 0.7:
            return "Reassured"
        elif label == 'NEGATIVE' and score > 0.7:
            return "Anxious"
        else:
            return "Neutral"
    except Exception as e:
        print(f"Transformer sentiment analysis failed: {e}")
        return analyze_sentiment_rule_based(text)


def analyze_sentiment_rule_based(text: str) -> str:
    """Rule-based sentiment analysis using keywords."""
    text_lower = text.lower()
    
    anxious_score = sum(1 for keyword in ANXIOUS_KEYWORDS if keyword in text_lower)
    reassured_score = sum(1 for keyword in REASSURED_KEYWORDS if keyword in text_lower)
    
    if anxious_score > reassured_score and anxious_score > 0:
        return "Anxious"
    elif reassured_score > anxious_score and reassured_score > 0:
        return "Reassured"
    else:
        return "Neutral"


def analyze_intent_rule_based(text: str) -> str:
    """Rule-based intent analysis."""
    text_lower = text.lower()
    
    symptom_score = sum(1 for keyword in SYMPTOM_REPORTING_KEYWORDS if keyword in text_lower)
    reassurance_score = sum(1 for keyword in REASSURANCE_SEEKING_KEYWORDS if keyword in text_lower)
    recovery_score = sum(1 for keyword in RECOVERY_CONFIRMING_KEYWORDS if keyword in text_lower)
    
    scores = {
        "Reporting symptoms": symptom_score,
        "Seeking reassurance": reassurance_score,
        "Confirming recovery": recovery_score
    }
    
    max_intent = max(scores, key=scores.get)
    
    if scores[max_intent] > 0:
        return max_intent
    else:
        return "Describing condition"


def analyze_sentiment_intent(processed_data: Dict[str, str]) -> Dict[str, str]:
    """
    Analyze sentiment and intent from patient text.
    
    Args:
        processed_data: Dictionary with processed text
        
    Returns:
        Dictionary with sentiment and intent
    """
    patient_text = processed_data.get("patient_text", "")
    
    if not patient_text:
        return {
            "Sentiment": "Neutral",
            "Intent": "Describing condition"
        }
    
    # Analyze sentiment
    sentiment = analyze_sentiment_transformers(patient_text)
    
    # Analyze intent
    intent = analyze_intent_rule_based(patient_text)
    
    return {
        "Sentiment": sentiment,
        "Intent": intent
    }


if __name__ == "__main__":
    # Test sentiment and intent analysis
    test_patient_text = "I'm doing much better, thank you. The neck pain has reduced significantly. I was worried it might take longer, but I'm really looking forward to getting back to normal activities."
    result = analyze_sentiment_intent({"patient_text": test_patient_text})
    print(json.dumps(result, indent=2))


