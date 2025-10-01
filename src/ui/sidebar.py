"""
Sidebar functionality for the Java Expert Chatbot Application
"""

import streamlit as st
import os
import json
from ui.components import render_empty_history_state, render_sample_question_item

def load_saved_histories():
    """Load all saved chat histories"""
    try:
        history_dir = "chat_history"
        if not os.path.exists(history_dir):
            return []
        
        histories = []
        for filename in os.listdir(history_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(history_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        histories.append({
                            "filename": filename,
                            "filepath": filepath,
                            "question": data.get("question", "Unknown Question"),
                            "display_name": data.get("display_name", data.get("question", "Unknown Question")),
                            "timestamp": data.get("timestamp", ""),
                            "chat_history": data.get("chat_history", [])
                        })
                except Exception as e:
                    continue
        
        # Sort by timestamp (newest first)
        histories.sort(key=lambda x: x["timestamp"], reverse=True)
        return histories
    except Exception as e:
        st.error(f"Error loading histories: {e}")
        return []

def update_history_name(filepath, new_name):
    """Update the display name of a saved history"""
    try:
        # Read existing data
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Update display name
        data["display_name"] = new_name
        
        # Save back to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        st.error(f"Error updating history name: {e}")
        return False

def delete_history_file(filepath):
    """Delete a saved history file"""
    try:
        os.remove(filepath)
        return True
    except Exception as e:
        st.error(f"Error deleting history: {e}")
        return False

def auto_save_current_chat():
    """Automatically save current chat if it exists"""
    from utils.chat_utils import save_chat_history
    
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

def render_sidebar_header():
    """Render the sidebar header"""
    st.markdown("""
    <div style="background: var(--primary-gradient); padding: 1.5rem; border-radius: var(--border-radius); margin-bottom: 1.5rem; text-align: center; color: white; box-shadow: var(--shadow-medium);">
        <h2 style="margin: 0; font-size: 1.5rem; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">🎛️ Control Panel</h2>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 0.9rem;">Manage your Java learning journey</p>
    </div>
    """, unsafe_allow_html=True)

def render_saved_histories_section():
    """Render the saved histories section in sidebar"""
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.subheader("📚 Saved Histories")
    saved_histories = load_saved_histories()
    
    if saved_histories:
        for i, history in enumerate(saved_histories[:10]):  # Show last 10
            # Create a container for each history item
            with st.container():
                # Create columns for buttons
                load_col, edit_col, delete_col = st.columns([4, 1, 1])
                
                with load_col:
                    # Use display_name if available, otherwise use question
                    display_name = history.get("display_name", history["question"])
                    display_text = display_name[:32] + "..." if len(display_name) > 32 else display_name
                    
                    if st.button(f"📄 {display_text}", key=f"load_history_{i}", help=f"Load: {display_name}"):
                        # Auto-save current chat before loading new one
                        auto_save_current_chat()
                        
                        # Load selected history
                        st.session_state.chat_history = history["chat_history"]
                        st.session_state.current_query = ""
                        st.session_state.current_chat_saved = True  # Mark as already saved
                        st.success("✅ History loaded!")
                        st.rerun()
                
                with edit_col:
                    if st.button("✏️", key=f"edit_history_{i}", help="Edit name"):
                        st.session_state[f"editing_history_{i}"] = True
                        st.rerun()
                
                with delete_col:
                    if st.button("🗑️", key=f"delete_history_{i}", help="Delete this history"):
                        if delete_history_file(history["filepath"]):
                            st.success("✅ Deleted!")
                            st.rerun()
                
                # Edit mode for this history item
                if st.session_state.get(f"editing_history_{i}", False):
                    st.markdown("**✏️ Edit History Name:**")
                    
                    # Create columns for edit input and buttons
                    input_col, save_col, cancel_col = st.columns([6, 1, 1])
                    
                    with input_col:
                        current_name = history.get("display_name", history["question"])
                        new_name = st.text_input(
                            "New name:",
                            value=current_name,
                            key=f"edit_input_{i}",
                            label_visibility="collapsed"
                        )
                    
                    with save_col:
                        if st.button("💾", key=f"save_edit_{i}", help="Save changes"):
                            if new_name.strip():
                                if update_history_name(history["filepath"], new_name.strip()):
                                    st.session_state[f"editing_history_{i}"] = False
                                    st.success("✅ Name updated!")
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to update name")
                            else:
                                st.warning("⚠️ Name cannot be empty")
                    
                    with cancel_col:
                        if st.button("❌", key=f"cancel_edit_{i}", help="Cancel editing"):
                            st.session_state[f"editing_history_{i}"] = False
                            st.rerun()
                    
                    st.markdown("---")
            
            # Add separator between items (only if not editing)
            if not st.session_state.get(f"editing_history_{i}", False):
                st.markdown("")
    else:
        render_empty_history_state()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_sample_questions_section():
    """Render the sample questions section in sidebar"""
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.subheader("💡 Sample Questions")
    sample_questions = [
        "How to implement pagination in Spring Boot?",
        "Create a secure REST API with JWT authentication",
        "How to use MapStruct for entity-DTO mapping?",
        "Implement global exception handling in Spring Boot",
        "Create a complete CRUD operation with security",
        "How to implement audit trail in Spring Boot?",
        "Best practices for Spring Boot validation"
    ]
    
    for i, question in enumerate(sample_questions):
        render_sample_question_item(question, i)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_sidebar():
    """Render the complete sidebar"""
    with st.sidebar:
        render_sidebar_header()
        render_saved_histories_section()
        render_sample_questions_section()