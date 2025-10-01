"""
Java Expert Chatbot - Main Application
Enterprise-ready Java development assistant with modern UI
"""

import streamlit as st
import os
import sys

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.chat import GroqJavaChatbot
from ui.styles import load_styles
from ui.components import render_header, render_footer
from ui.sidebar import render_sidebar
from ui.chat_interface import render_chat_interface

def configure_page():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="Java Expert Chatbot",
        page_icon="☕",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def initialize_chatbot():
    """Initialize the GroqJavaChatbot with API key"""
    try:
        # Try to get API key from secrets first, then from environment
        try:
            api_key = st.secrets["GROQ_API_KEY"]
        except:
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.getenv("GROQ_API_KEY")
            
        if not api_key:
            raise Exception("API key not found")
            
        return GroqJavaChatbot(api_key)
    except Exception as e:
        st.error("❌ API key not found. Please configure GROQ_API_KEY in Streamlit secrets or .env file.")
        st.stop()

def main():
    """Main application function"""
    # Configure page
    configure_page()
    
    # Load CSS styles
    load_styles()
    
    # Render header
    render_header()
    
    # Render sidebar
    render_sidebar()
    
    # Initialize chatbot
    chatbot = initialize_chatbot()
    
    # Render main chat interface
    render_chat_interface(chatbot)
    
    # Render footer
    render_footer()

if __name__ == "__main__":
    main()