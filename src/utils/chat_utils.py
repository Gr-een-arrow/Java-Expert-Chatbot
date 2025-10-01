"""
Chat utilities for the Java Expert Chatbot Application
"""

import re
import json
import os
from datetime import datetime
import streamlit as st

def extract_code_blocks(response):
    """Extract code blocks from the response"""
    code_pattern = r'```(\w+)?\n(.*?)```'
    code_blocks = re.findall(code_pattern, response, re.DOTALL)
    return code_blocks

def save_chat_history(question, chat_history):
    """Save chat history to a JSON file"""
    try:
        # Create history directory if it doesn't exist
        history_dir = "chat_history"
        if not os.path.exists(history_dir):
            os.makedirs(history_dir)
        
        # Create filename from question (first 50 chars, safe characters only)
        safe_question = re.sub(r'[^\w\s-]', '', question.strip())[:50]
        safe_question = re.sub(r'[-\s]+', '_', safe_question)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_question}_{timestamp}.json"
        filepath = os.path.join(history_dir, filename)
        
        # Prepare data to save
        save_data = {
            "question": question,
            "display_name": question,  # Add display_name field (same as question initially)
            "timestamp": datetime.now().isoformat(),
            "chat_history": chat_history
        }
        
        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        
        return filepath
    except Exception as e:
        st.error(f"Error saving history: {e}")
        return None