# 🚀 Quick Start Guide

## Installation (5 minutes)

### Option 1: Automated Setup (Recommended)
```bash
python setup.py
```

### Option 2: Manual Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Download spaCy model
python -m spacy download en_core_web_sm

# 3. Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# 4. (Optional) Install scispaCy for better medical NER
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_ner_bc5cdr_md-0.5.4.tar.gz
```

## Running the Application

### Method 1: Streamlit Web Interface (Easiest)
```bash
streamlit run app.py
```
Then open `http://localhost:8501` in your browser.

### Method 2: Command Line
```bash
python run.py data/raw_transcripts/sample_conversation.txt
```

### Method 3: Jupyter Notebook
1. Open `example_notebook.ipynb` in Jupyter
2. Run all cells

## Testing with Sample Data

The project includes a sample conversation at:
```
data/raw_transcripts/sample_conversation.txt
```

You can use this to test the system immediately.

## Input Format

Your conversation should follow this format:
```
Doctor: [doctor's dialogue]

Patient: [patient's dialogue]

Doctor: [more dialogue]
...
```

## Output Location

All results are saved in the `outputs/` directory:
- `medical_summary.json` - Structured medical report
- `sentiment_intent.json` - Sentiment and intent analysis
- `soap_note.json` - Complete SOAP note
- `complete_output.json` - All results combined

## Troubleshooting

### "spaCy model not found"
```bash
python -m spacy download en_core_web_sm
```

### "Transformers models downloading slowly"
First run downloads large models (~500MB-1GB). Be patient!

### "KeyBERT not working"
```bash
pip install keybert
```

### Memory errors
- Close other applications
- Use CPU instead of GPU
- Process shorter conversations

## Next Steps

1. ✅ Run the sample conversation
2. ✅ Try your own conversation
3. ✅ Explore the Streamlit interface
4. ✅ Check the Jupyter notebook example
5. ✅ Read the full README.md for details

## Need Help?

- Check `README.md` for detailed documentation
- Review `example_notebook.ipynb` for code examples
- Check the `src/` directory for module documentation


