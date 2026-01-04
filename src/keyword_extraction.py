"""
Keyword Extraction Module
Extracts important keywords using KeyBERT, TF-IDF, and noun chunking
"""

import json
import re
from typing import List, Dict
from collections import Counter

try:
    from keybert import KeyBERT
    KEYBERT_AVAILABLE = True
except ImportError:
    KEYBERT_AVAILABLE = False
    print("Warning: KeyBERT not available. Using fallback methods.")

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
    SPACY_AVAILABLE = True
except:
    SPACY_AVAILABLE = False
    nlp = None


def extract_keywords_keybert(text: str, top_n: int = 10) -> List[str]:
    """Extract keywords using KeyBERT."""
    if not KEYBERT_AVAILABLE:
        return []
    
    try:
        kw_model = KeyBERT()
        keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), top_n=top_n)
        return [kw[0] for kw in keywords]
    except Exception as e:
        print(f"KeyBERT extraction failed: {e}")
        return []


def extract_keywords_tfidf(text: str, top_n: int = 10) -> List[str]:
    """Extract keywords using TF-IDF."""
    if not SKLEARN_AVAILABLE:
        return []
    
    try:
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        if len(sentences) < 2:
            return []
        
        vectorizer = TfidfVectorizer(max_features=top_n, stop_words='english', ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform(sentences)
        
        # Get feature names
        feature_names = vectorizer.get_feature_names_out()
        
        # Get top keywords
        scores = tfidf_matrix.sum(axis=0).A1
        top_indices = scores.argsort()[-top_n:][::-1]
        
        keywords = [feature_names[i] for i in top_indices]
        return keywords
    except Exception as e:
        print(f"TF-IDF extraction failed: {e}")
        return []


def extract_noun_phrases(text: str, top_n: int = 10) -> List[str]:
    """Extract noun phrases using spaCy."""
    if not SPACY_AVAILABLE or nlp is None:
        return []
    
    try:
        doc = nlp(text)
        noun_phrases = []
        
        # Extract noun chunks
        for chunk in doc.noun_chunks:
            if len(chunk.text.split()) <= 3:  # Limit to 3-word phrases
                noun_phrases.append(chunk.text.lower())
        
        # Count and get most frequent
        phrase_counts = Counter(noun_phrases)
        top_phrases = [phrase for phrase, count in phrase_counts.most_common(top_n)]
        
        return top_phrases
    except Exception as e:
        print(f"Noun phrase extraction failed: {e}")
        return []


def extract_keywords(text: str, top_n: int = 15) -> List[str]:
    """
    Extract keywords using multiple methods and combine results.
    
    Args:
        text: Input text
        top_n: Number of keywords to extract
        
    Returns:
        List of extracted keywords
    """
    all_keywords = []
    
    # Try KeyBERT first
    keybert_kw = extract_keywords_keybert(text, top_n=top_n)
    all_keywords.extend(keybert_kw)
    
    # Try TF-IDF
    tfidf_kw = extract_keywords_tfidf(text, top_n=top_n)
    all_keywords.extend(tfidf_kw)
    
    # Try noun phrases
    noun_kw = extract_noun_phrases(text, top_n=top_n)
    all_keywords.extend(noun_kw)
    
    # Deduplicate and rank
    keyword_counts = Counter([kw.lower() for kw in all_keywords])
    
    # Filter out very common words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    filtered_keywords = [
        kw for kw, count in keyword_counts.most_common(top_n * 2)
        if kw not in stop_words and len(kw) > 2
    ]
    
    # Return top N unique keywords
    seen = set()
    result = []
    for kw in filtered_keywords:
        if kw not in seen:
            seen.add(kw)
            result.append(kw)
            if len(result) >= top_n:
                break
    
    return result


def extract_keywords_from_conversation(processed_data: Dict[str, str]) -> Dict[str, List[str]]:
    """
    Extract keywords from processed conversation.
    
    Args:
        processed_data: Dictionary with processed text
        
    Returns:
        Dictionary with extracted keywords
    """
    full_text = processed_data.get("full_text", "")
    
    keywords = extract_keywords(full_text, top_n=15)
    
    return {
        "Keywords": keywords
    }


if __name__ == "__main__":
    # Test keyword extraction
    test_text = "Patient experienced whiplash injury after car accident. Treatment includes physiotherapy sessions and painkillers. Full recovery expected within six months."
    result = extract_keywords(test_text)
    print(json.dumps({"Keywords": result}, indent=2))


