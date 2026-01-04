# 🏥 Swasthya – NLP System

## Overview
This project implements an AI-based Swasthya system that processes doctor–patient conversations to extract medical entities, generate structured summaries, analyze patient sentiment and intent, and create SOAP clinical notes.

##Screenshots:
<img width="1919" height="836" alt="image" src="https://github.com/user-attachments/assets/81ffec0d-c51c-45c6-ac7f-b78f3ecb8ee4" />
<img width="1919" height="758" alt="image" src="https://github.com/user-attachments/assets/19745bf3-a4a6-4daf-88c4-d6994418840c" />
<img width="1909" height="857" alt="image" src="https://github.com/user-attachments/assets/73340e54-7162-4f7e-b90c-63c0f050875b" />


## Features
- **Medical Named Entity Recognition (NER)**: Extracts symptoms, diagnosis, treatment, and prognosis
- **Keyword Extraction**: Uses KeyBERT, TF-IDF, and noun chunking
- **Medical Text Summarization**: Generates concise summaries using BART
- **Sentiment & Intent Analysis**: Analyzes patient emotional state and communication intent
- **SOAP Note Generation**: Creates structured clinical notes (Subjective, Objective, Assessment, Plan)

## Tech Stack
- **Python 3.8+**
- **spaCy & scispaCy**: Medical NLP and entity recognition
- **Transformers**: BERT, BART for summarization and sentiment analysis
- **KeyBERT**: Keyword extraction
- **Streamlit**: Web interface
- **NLTK**: Text processing utilities

## Installation

### 1. Clone or Download the Project
```bash
cd Swasthya
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Download spaCy Models
```bash
python -m spacy download en_core_web_sm
```

### 4. (Optional) Install scispaCy Medical Model
For better medical NER, install the scispaCy model:
```bash
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_ner_bc5cdr_md-0.5.4.tar.gz
```

### 5. Download NLTK Data
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

## Project Structure

```
physician-notetaker/
│
├── data/
│   ├── raw_transcripts/
│   │   └── sample_conversation.txt
│   └── processed/
│
├── models/
│   ├── ner/
│   ├── sentiment/
│   └── summarization/
│
├── src/
│   ├── __init__.py
│   ├── preprocessing.py          # Text preprocessing
│   ├── ner_extraction.py        # Medical NER
│   ├── keyword_extraction.py    # Keyword extraction
│   ├── summarization.py         # Text summarization
│   ├── sentiment_intent.py      # Sentiment & intent analysis
│   ├── soap_generator.py        # SOAP note generation
│   └── pipeline.py              # Main pipeline
│
├── outputs/                     # Generated outputs
│
├── requirements.txt
├── README.md
├── run.py                       # Command-line execution
└── app.py                       # Streamlit web app
```

## Usage

### Method 1: Streamlit Web Interface (Recommended)
```bash
streamlit run app.py
```
Then open your browser to `http://localhost:8501`

### Method 2: Command Line
```bash
python run.py data/raw_transcripts/sample_conversation.txt
```

### Method 3: Jupyter Notebook
You can import and use the modules in a Jupyter notebook:
```python
from src.pipeline import run_pipeline

result = run_pipeline("data/raw_transcripts/sample_conversation.txt")
print(result)
```

## Input Format

The system expects conversation text with speaker tags:
```
Doctor: Good morning, Janet. How are you feeling today?

Patient: Good morning, doctor. I'm doing much better, thank you.

Doctor: That's excellent news. Can you tell me about the back pain?
```

## Output

The system generates several output files in the `outputs/` directory:

1. **medical_summary.json**: Structured medical report
2. **sentiment_intent.json**: Sentiment and intent analysis
3. **soap_note.json**: Complete SOAP clinical note
4. **complete_output.json**: All results combined

### Example Output Structure

```json
{
  "Medical_Report": {
    "Patient_Name": "Janet Jones",
    "Symptoms": ["neck pain", "back pain"],
    "Diagnosis": "whiplash injury",
    "Treatment": ["physiotherapy", "painkillers"],
    "Prognosis": "Full recovery expected within six months"
  },
  "Sentiment_Intent": {
    "Sentiment": "Reassured",
    "Intent": "Confirming recovery"
  },
  "SOAP_Note": {
    "Subjective": {...},
    "Objective": {...},
    "Assessment": {...},
    "Plan": {...}
  }
}
```

## Module Details

### 1. Preprocessing (`src/preprocessing.py`)
- Removes speaker tags
- Normalizes text
- Segments doctor vs patient dialogue

### 2. NER Extraction (`src/ner_extraction.py`)
- Uses scispaCy or spaCy for entity recognition
- Extracts: Symptoms, Diagnosis, Treatment, Prognosis
- Keyword-based fallback for better coverage

### 3. Keyword Extraction (`src/keyword_extraction.py`)
- KeyBERT for semantic keyword extraction
- TF-IDF for statistical keyword extraction
- Noun phrase chunking for phrase extraction

### 4. Summarization (`src/summarization.py`)
- Uses BART-large-CNN for abstractive summarization
- Falls back to extractive summarization if transformers unavailable

### 5. Sentiment & Intent (`src/sentiment_intent.py`)
- DistilBERT for sentiment analysis
- Rule-based intent classification
- Categories: Anxious, Neutral, Reassured

### 6. SOAP Generator (`src/soap_generator.py`)
- Maps conversation to SOAP structure
- Extracts subjective, objective, assessment, and plan sections

### 7. Pipeline (`src/pipeline.py`)
- Orchestrates all modules
- Combines results into final output
- Saves JSON files

## Assumptions & Limitations

### Assumptions
- Conversations follow a structured format with speaker tags
- Medical terminology is used appropriately
- Pre-trained models are sufficient for general medical conversations

### Limitations
- **Not intended for real clinical deployment** without proper validation
- Requires human validation for medical safety
- Pre-trained models may not cover all medical specialties
- Performance depends on conversation quality and clarity
- May not handle very specialized medical terminology

## Troubleshooting

### Issue: spaCy model not found
```bash
python -m spacy download en_core_web_sm
```

### Issue: Transformers models downloading slowly
The first run will download models (~500MB-1GB). Be patient or use a faster internet connection.

### Issue: KeyBERT not working
Install KeyBERT: `pip install keybert`

### Issue: Memory errors
Reduce batch sizes or use smaller models. Consider using CPU instead of GPU.

## Future Enhancements
- [ ] Support for multiple languages
- [ ] Integration with Electronic Health Records (EHR)
- [ ] Real-time conversation processing
- [ ] Custom model fine-tuning
- [ ] Multi-specialty support
- [ ] HIPAA compliance features

## Contributing
This is an educational project. Contributions and improvements are welcome!

## License
This project is for educational purposes only.

## Disclaimer
**This system is for educational and research purposes only.**
**Not intended for real clinical deployment without proper validation and regulatory approval.**
**Always consult with medical professionals for actual clinical decisions.**

## Contact
For questions or issues, please refer to the project documentation or create an issue in the repository.


