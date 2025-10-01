"""
Chat interface for the Java Expert Chatbot Application
"""

import streamlit as st
import re
import json
import os
from utils.chat_utils import extract_code_blocks, save_chat_history
from ui.components import (
    render_user_input_section, render_action_center, render_user_message,
    render_assistant_response_header, render_loading_indicator, 
    render_chat_history_header, render_code_block_with_copy
)

def initialize_session_state():
    """Initialize session state variables"""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "selected_question" not in st.session_state:
        st.session_state.selected_question = ""
    if "copied_code" not in st.session_state:
        st.session_state.copied_code = {}
    if "current_query" not in st.session_state:
        st.session_state.current_query = ""
    if "current_chat_saved" not in st.session_state:
        st.session_state.current_chat_saved = False

def auto_save_current_chat():
    """Automatically save current chat if it exists"""
    if (len(st.session_state.chat_history) > 0 and 
        not st.session_state.get("current_chat_saved", False)):
        
        # Get the first user question as the history name
        first_question = None
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                first_question = message["content"]
                break
        
        if first_question:
            saved_file = save_chat_history(first_question, st.session_state.chat_history)
            if saved_file:
                # Mark current chat as saved
                st.session_state.current_chat_saved = True
                # Show notification
                st.toast(f"💾 Previous chat auto-saved: {os.path.basename(saved_file)[:30]}...", icon="💾")
                return True
    return False

def handle_sample_question():
    """Handle selected question from sidebar"""
    if st.session_state.selected_question:
        # Auto-save current chat before switching to new question
        if st.session_state.chat_history and not st.session_state.current_chat_saved:
            auto_save_current_chat()
        
        # Clear current chat and set new question
        st.session_state.chat_history = []
        st.session_state.current_query = st.session_state.selected_question
        st.session_state.selected_question = ""
        st.session_state.current_chat_saved = False
        st.session_state.copied_code = {}

def render_input_section():
    """Render the user input section"""
    render_user_input_section()
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_query = st.text_area(
            "Your Question:",
            value=st.session_state.current_query,
            height=120,
            placeholder="🚀 Example: How to implement JWT authentication in Spring Boot?\n💡 Or: Best practices for RESTful API design?\n🔒 Or: How to secure a Spring Boot application?",
            key="user_input",
            label_visibility="collapsed"
        )
        
        # Update current_query when user types
        if user_query != st.session_state.current_query:
            st.session_state.current_query = user_query
    
    with col2:
        render_action_center()
        
        st.write("")  # Spacing
        submit_button = st.button("🚀 Ask Expert", type="primary", use_container_width=True)
        
        # Action buttons with enhanced styling
        st.markdown('<div style="margin-top: 1rem;">', unsafe_allow_html=True)
        col2a, col2b = st.columns(2)
        with col2a:
            clear_button = st.button("🗑️ Clear", use_container_width=True, help="Clear current conversation")
        with col2b:
            # Manual save button (optional now)
            save_button = st.button("💾 Save", use_container_width=True, 
                                   disabled=len(st.session_state.chat_history) == 0 or st.session_state.current_chat_saved,
                                   help="Save current conversation")
        st.markdown('</div>', unsafe_allow_html=True)
    
    return submit_button, clear_button, save_button

def handle_manual_save():
    """Handle manual save button click"""
    if st.session_state.chat_history and not st.session_state.current_chat_saved:
        # Get the first user question as the history name
        first_question = None
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                first_question = message["content"]
                break
        
        if first_question:
            saved_file = save_chat_history(first_question, st.session_state.chat_history)
            if saved_file:
                st.session_state.current_chat_saved = True
                st.success(f"✅ History saved as: {os.path.basename(saved_file)}")
                st.rerun()
        else:
            st.warning("⚠️ No questions found in chat history.")

def handle_clear_chat():
    """Handle clear chat button click"""
    # Auto-save before clearing
    auto_save_current_chat()
    
    # Clear everything
    st.session_state.chat_history = []
    st.session_state.copied_code = {}
    st.session_state.current_query = ""
    st.session_state.current_chat_saved = False
    st.rerun()

def stream_with_progress(chatbot, streaming_container):
    """Handle streaming response with progress indicators"""
    # Create streaming container
    progress_container = st.container()
    with progress_container:
        render_loading_indicator()
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Progress updates
    status_text.text("🔍 Analyzing your question...")
    progress_bar.progress(10)
    
    status_text.text("🧠 Generating enterprise-grade solution...")
    progress_bar.progress(30)
    
    status_text.text("🔒 Adding security best practices...")
    progress_bar.progress(50)
    
    status_text.text("📝 Creating complete code examples...")
    progress_bar.progress(70)
    
    # Get the actual response
    response = chatbot.stream_response(
        st.session_state.current_query, 
        print_to_terminal=True,
        streamlit_container=streaming_container
    )
    
    progress_bar.progress(100)
    status_text.text("✅ Response completed!")
    
    # Clean up progress indicators after a short delay
    import time
    time.sleep(1)
    progress_bar.empty()
    status_text.empty()
    
    return response

def process_user_query(chatbot):
    """Process user query and generate response"""
    if not st.session_state.current_query.strip():
        st.warning("⚠️ Please enter a question.")
        return
    
    # Check if this is a new question when there's already a chat history
    if (len(st.session_state.chat_history) > 0 and 
        not st.session_state.current_chat_saved and
        st.session_state.current_query not in [msg["content"] for msg in st.session_state.chat_history if msg["role"] == "user"]):
        
        # Auto-save current chat before starting new question
        auto_save_current_chat()
        
        # Clear chat for new question
        st.session_state.chat_history = []
        st.session_state.current_chat_saved = False
    
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "content": st.session_state.current_query})
    
    # Show streaming response in real-time
    st.markdown("---")
    render_user_message(st.session_state.current_query)
    render_assistant_response_header()
    
    # Create streaming container
    streaming_container = st.empty()
    
    # Get streaming response
    response = stream_with_progress(chatbot, streaming_container)
    
    # Add bot response to history
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    # Clear the current query after processing
    st.session_state.current_query = ""
    
    # Rerun to show the new response in proper format
    st.rerun()

def display_chat_history():
    """Display the chat history with enhanced styling"""
    if not st.session_state.chat_history:
        return
    
    # Show save status with modern design
    render_chat_history_header(st.session_state.current_chat_saved)
    
    for i, message in enumerate(st.session_state.chat_history):
        if message["role"] == "user":
            render_user_message(message["content"])
        
        else:  # assistant
            render_assistant_response_header()
            
            # Display the response with code highlighting
            response_content = message["content"]
            
            # Extract and display code blocks separately for copy functionality
            code_blocks = extract_code_blocks(response_content)
            
            if code_blocks:
                # Display response without code blocks first
                text_without_code = re.sub(r'```(\w+)?\n(.*?)```', '\n[CODE BLOCK BELOW]\n', response_content, flags=re.DOTALL)
                st.markdown(text_without_code)
                
                # Display each code block with copy functionality
                for j, (language, code) in enumerate(code_blocks):
                    render_code_block_with_copy(code, language, i, j)
            else:
                # No code blocks, display normally
                st.markdown(response_content)
            
            st.markdown("---")

def render_chat_interface(chatbot):
    """Render the complete chat interface"""
    # Initialize session state
    initialize_session_state()
    
    # Handle sample question selection
    handle_sample_question()
    
    # Render input section and get button states
    submit_button, clear_button, save_button = render_input_section()
    
    # Handle button clicks
    if save_button:
        handle_manual_save()
    
    if clear_button:
        handle_clear_chat()
    
    if submit_button:
        process_user_query(chatbot)
    
    # Display chat history
    display_chat_history()