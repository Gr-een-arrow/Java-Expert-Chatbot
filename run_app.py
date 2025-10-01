"""
Java Expert Chatbot - Alternative Entry Point
Alternative way to run the organized application
"""

import os
import sys

# Add src directory to Python path to allow imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

if __name__ == "__main__":
    try:
        from main import main
        main()
    except ImportError as e:
        print(f"❌ Error: {e}")
        print("Please run: streamlit run src/main.py")
        sys.exit(1)