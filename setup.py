"""
Setup script for Swasthya
Helps install dependencies and download required models
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"\n{'='*60}")
    print(f"📦 {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f" Error: {e.stderr}")
        return False

def main():
    """Main setup function."""
    print("🏥 Swasthya - Setup Script")
    print("="*60)
    
    # Step 1: Install Python packages
    print("\nStep 1: Installing Python packages...")
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", 
                      "Installing requirements"):
        print("⚠️  Some packages may have failed to install. Please check manually.")
    
    # Step 2: Download spaCy model
    print("\nStep 2: Downloading spaCy model...")
    run_command(f"{sys.executable} -m spacy download en_core_web_sm", 
               "Downloading en_core_web_sm model")
    
    # Step 3: Download NLTK data
    print("\nStep 3: Downloading NLTK data...")
    nltk_script = """
import nltk
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    print(" NLTK data downloaded successfully")
except Exception as e:
    print(f"⚠️  NLTK download error: {e}")
"""
    run_command(f"{sys.executable} -c \"{nltk_script}\"", 
               "Downloading NLTK data")
    
    # Step 4: Optional scispaCy model
    print("\nStep 4: Optional - Installing scispaCy medical model...")
    print("(This is optional but recommended for better medical NER)")
    response = input("Install scispaCy model? (y/n): ").strip().lower()
    if response == 'y':
        run_command(
            f"{sys.executable} -m pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_ner_bc5cdr_md-0.5.4.tar.gz",
            "Installing scispaCy medical model"
        )
    else:
        print(" Skipping scispaCy model installation")
    
    # Create necessary directories
    print("\nStep 5: Creating directories...")
    directories = [
        "data/raw_transcripts",
        "data/processed",
        "outputs",
        "models/ner",
        "models/sentiment",
        "models/summarization"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f" Created: {directory}")
    
    print("\n" + "="*60)
    print(" Setup completed!")
    print("="*60)
    print("\nNext steps:")
    print("1. Run Streamlit app: streamlit run app.py")
    print("2. Or run command line: python run.py")
    print("3. Or use in Jupyter: see example_notebook.ipynb")

if __name__ == "__main__":
    main()


