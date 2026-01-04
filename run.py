"""
Main execution file for Swasthya
"""

import sys
import os
from src.pipeline import run_pipeline

def main():
    """Main function to run the pipeline."""
    # Default input file
    input_file = "data/raw_transcripts/sample_conversation.txt"
    
    # Allow command-line argument for custom file
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(input_file):
        print(f"Error: File not found: {input_file}")
        print("Usage: python run.py [path_to_conversation_file]")
        sys.exit(1)
    
    # Run pipeline
    try:
        result = run_pipeline(input_file)
        print("\n=== Pipeline Execution Complete ===")
        print(f"Check the 'outputs/' directory for results.")
    except Exception as e:
        print(f"Error running pipeline: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()


