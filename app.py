"""
Streamlit Web Application for Swasthya
"""

import streamlit as st
import json
import os
from datetime import datetime
# from src.pipeline import run_pipeline  # Commented out for demo
# from src.preprocessing import preprocess_conversation
# from src.ner_extraction import extract_ner_from_conversation
# from src.keyword_extraction import extract_keywords_from_conversation
# from src.summarization import summarize_conversation
# from src.sentiment_intent import analyze_sentiment_intent
# from src.soap_generator import generate_soap_note

def generate_medicine_recommendations(symptoms, diagnosis):
    """Generate simple medicine recommendations based on symptoms."""
    recommendations = []

    # Simple symptom to medicine mapping
    medicine_map = {
        'fever': [
            {'medicine': 'Paracetamol 500mg', 'dosage': '1 tablet every 4-6 hours'},
            {'medicine': 'Ibuprofen 400mg', 'dosage': '1 tablet every 6-8 hours'}
        ],
        'headache': [
            {'medicine': 'Paracetamol 500mg', 'dosage': '1 tablet every 4-6 hours'},
            {'medicine': 'Ibuprofen 400mg', 'dosage': '1 tablet every 6-8 hours'}
        ],
        'pain': [
            {'medicine': 'Ibuprofen 400mg', 'dosage': '1 tablet every 6-8 hours'},
            {'medicine': 'Paracetamol 500mg', 'dosage': '1 tablet every 4-6 hours'}
        ],
        'cough': [
            {'medicine': 'Cough syrup', 'dosage': '10ml every 4-6 hours'},
            {'medicine': 'Dextromethorphan', 'dosage': '10-20mg every 4 hours'}
        ],
        'cold': [
            {'medicine': 'Paracetamol 500mg', 'dosage': '1 tablet every 4-6 hours'},
            {'medicine': 'Vitamin C tablets', 'dosage': '1 tablet daily'}
        ],
        'sore throat': [
            {'medicine': 'Throat lozenges', 'dosage': '1 lozenge every 2-3 hours'},
            {'medicine': 'Paracetamol 500mg', 'dosage': '1 tablet every 4-6 hours'}
        ],
        'nausea': [
            {'medicine': 'Ondansetron 4mg', 'dosage': '1 tablet every 8 hours'},
            {'medicine': 'Dimenhydrinate 50mg', 'dosage': '1 tablet every 4-6 hours'}
        ],
        'vomiting': [
            {'medicine': 'Ondansetron 4mg', 'dosage': '1 tablet every 8 hours'},
            {'medicine': 'Domperidone 10mg', 'dosage': '1 tablet every 8 hours'}
        ],
        'diarrhea': [
            {'medicine': 'Oral rehydration salts', 'dosage': '1 packet in water every hour'},
            {'medicine': 'Loperamide 2mg', 'dosage': '1 tablet after each loose stool'}
        ],
        'constipation': [
            {'medicine': 'Lactulose syrup', 'dosage': '15-30ml daily'},
            {'medicine': 'Bisacodyl 5mg', 'dosage': '1 tablet daily'}
        ],
        'fatigue': [
            {'medicine': 'Multivitamin', 'dosage': '1 tablet daily'},
            {'medicine': 'Iron supplement', 'dosage': 'As prescribed'}
        ],
        'insomnia': [
            {'medicine': 'Melatonin 3mg', 'dosage': '1 tablet 30 minutes before sleep'},
            {'medicine': 'Diphenhydramine 25mg', 'dosage': '1 tablet before sleep'}
        ],
        'anxiety': [
            {'medicine': 'Alprazolam 0.25mg', 'dosage': 'As prescribed by doctor'},
            {'medicine': 'Sertraline 25mg', 'dosage': 'As prescribed by doctor'}
        ],
        'depression': [
            {'medicine': 'Sertraline 25mg', 'dosage': 'As prescribed by doctor'},
            {'medicine': 'Escitalopram 5mg', 'dosage': 'As prescribed by doctor'}
        ],
        'allergy': [
            {'medicine': 'Cetirizine 10mg', 'dosage': '1 tablet daily'},
            {'medicine': 'Loratadine 10mg', 'dosage': '1 tablet daily'}
        ],
        'rash': [
            {'medicine': 'Cetirizine 10mg', 'dosage': '1 tablet daily'},
            {'medicine': 'Hydrocortisone cream', 'dosage': 'Apply 2-3 times daily'}
        ],
        'infection': [
            {'medicine': 'Amoxicillin 500mg', 'dosage': '1 capsule every 8 hours'},
            {'medicine': 'Azithromycin 500mg', 'dosage': '1 tablet daily for 3 days'}
        ]
    }

    # Check each symptom against our medicine map
    for symptom in symptoms:
        symptom_lower = symptom.lower()
        for key in medicine_map:
            if key in symptom_lower:
                recommendations.extend(medicine_map[key])
                break

    # Remove duplicates
    seen = set()
    unique_recommendations = []
    for rec in recommendations:
        rec_tuple = (rec['medicine'], rec['dosage'])
        if rec_tuple not in seen:
            seen.add(rec_tuple)
            unique_recommendations.append(rec)

    return unique_recommendations[:4]  # Limit to 4 recommendations

def run_pipeline(file_path):
    """Mock pipeline function for demo purposes."""
    # Mock analysis result
    mock_result = {
        'NER_Extraction': {
            'Symptoms': ['fever', 'headache', 'cough'],
            'Diagnosis': ['Common Cold', 'Viral Infection']
        },
        'Sentiment_Intent': {
            'Sentiment': 'Anxious',
            'Intent': 'Seeking medical advice'
        },
        'Keywords': ['fever', 'headache', 'cough', 'pain'],
        'Summary': 'Patient is experiencing fever, headache, and cough. Appears to be anxious about their condition.',
        'SOAP_Note': {
            'Subjective': 'Patient reports fever, headache, and cough for 2 days.',
            'Objective': 'Patient appears uncomfortable.',
            'Assessment': 'Viral upper respiratory infection.',
            'Plan': 'Recommend rest, hydration, and symptomatic treatment.'
        }
    }
    return mock_result

# Page configuration
st.set_page_config(
    page_title="Swasthya - Medicine Recommendation AI",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }

    /* Header Styles */
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(45deg, #ffffff, #e0e7ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .subtitle {
        font-size: 1.2rem;
        color: #e0e7ff;
        text-align: center;
        margin-bottom: 2rem;
        opacity: 0.9;
    }

    /* Card Styles */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }

    .result-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .result-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
    }

    /* Section Headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: white;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #3b82f6;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        transition: transform 0.2s ease;
    }

    .metric-card:hover {
        transform: scale(1.05);
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #059669, #047857);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
    }

    /* Tab Styles */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 0.5rem;
        backdrop-filter: blur(10px);
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #e0e7ff;
        font-weight: 500;
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: rgba(255, 255, 255, 0.2);
        color: white;
    }

    /* Expander Styles */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }

    /* Input Styles */
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 12px;
        color: white;
        backdrop-filter: blur(10px);
    }

    .stTextArea > div > div > textarea::placeholder {
        color: rgba(255, 255, 255, 0.6);
    }

    /* Radio Button Styles */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* Success/Error Messages */
    .stSuccess, .stError {
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }

    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #10b981, #3b82f6);
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #e0e7ff;
        margin-top: 3rem;
        opacity: 0.8;
        font-size: 0.9rem;
    }

    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Conversation Input Card */
    .conversation-input-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border: 2px solid rgba(255, 255, 255, 0.8);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }

    .input-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #3b82f6;
    }

    /* Symptoms Section */
    .symptoms-section {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }

    .symptoms-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.8rem;
        margin-top: 1rem;
    }

    .symptom-tag {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 500;
        font-size: 0.9rem;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
    }

    /* Medicine Section */
    .medicine-section {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }

    .symptom-medicine {
        background: rgba(16, 185, 129, 0.05);
        border-left: 4px solid #10b981;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 8px;
    }

    .symptom-medicine h4 {
        color: #065f46;
        margin-bottom: 0.5rem;
    }

    .medicine-item {
        background: rgba(16, 185, 129, 0.1);
        padding: 0.5rem;
        margin: 0.3rem 0;
        border-radius: 6px;
        color: #065f46;
    }

    /* Disclaimer Section */
    .disclaimer-section {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid #ef4444;
        border-radius: 12px;
        padding: 1rem;
        margin: 1.5rem 0;
    }

    /* Placeholder Section */
    .placeholder-section {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        text-align: center;
    }

    /* No symptoms section */
    .no-symptoms {
        background: rgba(156, 163, 175, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        text-align: center;
    }

    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">💊 Swasthya</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-Powered Medicine Recommendation System</p>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📋 Navigation")
st.sidebar.markdown("---")

# Navigation options
nav_option = st.sidebar.radio(
    "Choose a section:",
    ["Home", "About", "How to Use"],
    index=0
)

st.sidebar.markdown("---")

if nav_option == "About":
    st.sidebar.markdown("### 💊 About Swasthya")
    st.sidebar.markdown("""
    **Swasthya** is an AI-powered medicine recommendation system that analyzes 
    medical conversations and suggests appropriate medications based on detected symptoms.
    
    **Key Features:**
    - Symptom detection from conversations
    - Medicine recommendations with dosages
    - Real-time analysis
    - User-friendly interface
    """)

elif nav_option == "How to Use":
    st.sidebar.markdown("### 📋 How to Use")
    st.sidebar.markdown("""
    1. **Enter Conversation**: Type or paste a doctor-patient conversation
    2. **Automatic Analysis**: The system detects symptoms in real-time
    3. **View Medicines**: See suggested medicines with dosages for each symptom
    4. **Consult Doctor**: Always verify with healthcare professional
    
    **Example Conversation:**
    ```
    Doctor: How are you feeling?
    Patient: I have fever and headache, also coughing a lot.
    ```
    """)

# Main content area
if nav_option == "Home":
    st.markdown('<div class="conversation-input-card">', unsafe_allow_html=True)
    st.markdown('<div class="input-header">💬 Enter Medical Conversation</div>', unsafe_allow_html=True)

    conversation_text = st.text_area(
        "Enter your medical conversation:",
        height=200,
        placeholder="Type your medical conversation here...\n\nExample: Doctor: How are you feeling?\nPatient: I have fever and headache...",
        key="conversation_input"
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # Dynamic analysis section
    if conversation_text:
        # Analyze conversation directly (mock analysis)
        with st.spinner("🔍 Analyzing conversation..."):
            try:
                # Simple symptom detection from text
                text_lower = conversation_text.lower()
                detected_symptoms = []

                symptom_keywords = {
                    'fever': ['fever', 'temperature', 'hot'],
                    'headache': ['headache', 'head ache', 'migraine'],
                    'cough': ['cough', 'coughing'],
                    'cold': ['cold', 'runny nose', 'sneezing'],
                    'pain': ['pain', 'hurts', 'ache'],
                    'nausea': ['nausea', 'sick', 'queasy'],
                    'vomiting': ['vomit', 'throw up', 'nauseous'],
                    'diarrhea': ['diarrhea', 'loose motion'],
                    'fatigue': ['tired', 'fatigue', 'weak'],
                    'rash': ['rash', 'skin irritation'],
                    'infection': ['infection', 'infected']
                }

                for symptom, keywords in symptom_keywords.items():
                    if any(keyword in text_lower for keyword in keywords):
                        detected_symptoms.append(symptom.title())

                if detected_symptoms:
                    # Symptoms Display
                    st.markdown('<div class="symptoms-section">', unsafe_allow_html=True)
                    st.markdown('<div class="section-header">🔍 Detected Symptoms</div>', unsafe_allow_html=True)

                    symptoms_html = '<div class="symptoms-container">'
                    for symptom in detected_symptoms:
                        symptoms_html += f'<span class="symptom-tag">{symptom}</span>'
                    symptoms_html += '</div>'
                    st.markdown(symptoms_html, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                # Medicine Recommendations
                st.markdown('<div class="medicine-section">', unsafe_allow_html=True)
                st.markdown('<div class="section-header">💊 Medicine Recommendations</div>', unsafe_allow_html=True)

                for symptom in detected_symptoms:
                    symptom_lower = symptom.lower()
                    st.markdown(f'<div class="symptom-medicine">', unsafe_allow_html=True)
                    st.markdown(f'<h4>🩺 For {symptom}:</h4>', unsafe_allow_html=True)

                    # Medicine mapping
                    medicine_map = {
                        'Fever': ['Paracetamol 500mg - 1 tablet every 4-6 hours', 'Ibuprofen 400mg - 1 tablet every 6-8 hours'],
                        'Headache': ['Paracetamol 500mg - 1 tablet every 4-6 hours', 'Ibuprofen 400mg - 1 tablet every 6-8 hours'],
                        'Pain': ['Ibuprofen 400mg - 1 tablet every 6-8 hours', 'Paracetamol 500mg - 1 tablet every 4-6 hours'],
                        'Cough': ['Cough syrup - 10ml every 4-6 hours', 'Dextromethorphan - 10-20mg every 4 hours'],
                        'Cold': ['Paracetamol 500mg - 1 tablet every 4-6 hours', 'Vitamin C - 1 tablet daily'],
                        'Nausea': ['Ondansetron 4mg - 1 tablet every 8 hours', 'Dimenhydrinate 50mg - 1 tablet every 4-6 hours'],
                        'Vomiting': ['Ondansetron 4mg - 1 tablet every 8 hours', 'Domperidone 10mg - 1 tablet every 8 hours'],
                        'Diarrhea': ['Oral rehydration salts - 1 packet in water every hour', 'Loperamide 2mg - 1 tablet after each loose stool'],
                        'Fatigue': ['Multivitamin - 1 tablet daily', 'Iron supplement - As prescribed'],
                        'Rash': ['Cetirizine 10mg - 1 tablet daily', 'Hydrocortisone cream - Apply 2-3 times daily'],
                        'Infection': ['Amoxicillin 500mg - 1 capsule every 8 hours', 'Azithromycin 500mg - 1 tablet daily for 3 days']
                    }

                    found_medicine = False
                    for key, medicines in medicine_map.items():
                        if key.lower() in symptom_lower:
                            for medicine in medicines:
                                st.markdown(f'<div class="medicine-item">• <strong>{medicine}</strong></div>', unsafe_allow_html=True)
                            found_medicine = True
                            break

                    if not found_medicine:
                        st.markdown('<div class="medicine-item">• <em>Consult a doctor for appropriate medication</em></div>', unsafe_allow_html=True)

                    st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)

                # Disclaimer
                st.markdown('<div class="disclaimer-section">', unsafe_allow_html=True)
                st.error("**MEDICAL DISCLAIMER** These are general recommendations only. Always consult a qualified healthcare professional before taking any medication. This AI system is for informational purposes and does not replace professional medical advice.")
                st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Error analyzing conversation: {str(e)}")

        if not detected_symptoms:
            st.markdown('<div class="no-symptoms">', unsafe_allow_html=True)
            st.info("🤔 No specific symptoms detected in the conversation. Try mentioning symptoms like fever, headache, cough, etc.")
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        # Placeholder when no text is entered
        st.markdown('<div class="placeholder-section">', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; color: rgba(255,255,255,0.7); padding: 3rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">&#128172;</div>
            <div style="font-size: 1.2rem;">Enter a medical conversation above to get medicine recommendations</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    '<div class="footer">'
    'Swasthya - AI Medical Assistant | Built with love using Streamlit'
    '</div>',
    unsafe_allow_html=True
)


