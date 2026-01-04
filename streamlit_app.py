import streamlit as st
import os
import json
from src.pipeline import run_pipeline

st.title("Swasthya - Medical Conversation Analyzer")

st.markdown("""
This app processes medical conversations to extract key information including:
- Named Entity Recognition (NER)
- Keywords
- Medical Summary
- Sentiment & Intent Analysis
- SOAP Notes
""")

# File selection
st.header("Select Input File")

option = st.radio("Choose input method:", ("Upload a file", "Select from existing files"))

input_file = None

if option == "Upload a file":
    uploaded_file = st.file_uploader("Choose a text file", type="txt")
    if uploaded_file is not None:
        # Save uploaded file temporarily
        temp_path = "temp_uploaded_file.txt"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        input_file = temp_path
        st.success(f"File uploaded: {uploaded_file.name}")

elif option == "Select from existing files":
    # List files in data/raw_transcripts/
    transcript_dir = "data/raw_transcripts"
    if os.path.exists(transcript_dir):
        files = [f for f in os.listdir(transcript_dir) if f.endswith('.txt')]
        if files:
            selected_file = st.selectbox("Choose a file:", files)
            input_file = os.path.join(transcript_dir, selected_file)
        else:
            st.error("No .txt files found in data/raw_transcripts/")
    else:
        st.error("data/raw_transcripts/ directory not found")

# Run button
if input_file and st.button("Run Analysis"):
    with st.spinner("Processing conversation... This may take a few minutes."):
        try:
            result = run_pipeline(input_file)

            st.success("Analysis complete!")

            # Display results
            st.header("Results")

            # Medical Report
            with st.expander("Medical Report", expanded=True):
                st.json(result["Medical_Report"])

            # NER Extraction
            with st.expander("Named Entity Recognition"):
                st.json(result["NER_Extraction"])

            # Keywords
            with st.expander("Keywords"):
                st.json(result["Keywords"])

            # Summary
            with st.expander("Medical Summary"):
                st.json(result["Summary"])

            # Sentiment & Intent
            with st.expander("Sentiment & Intent Analysis"):
                st.json(result["Sentiment_Intent"])

            # SOAP Note
            with st.expander("SOAP Note"):
                st.json(result["SOAP_Note"])

            # Download complete results
            st.download_button(
                label="Download Complete Results",
                data=json.dumps(result, indent=2),
                file_name="analysis_results.json",
                mime="application/json"
            )

        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            st.exception(e)

# Clean up temp file if uploaded
if option == "Upload a file" and input_file and os.path.exists("temp_uploaded_file.txt"):
    os.remove("temp_uploaded_file.txt")