import streamlit as st
import re
import json
import os
from datetime import datetime
from chat import GroqJavaChatbot

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

def main():
    st.set_page_config(
        page_title="Java Expert Chatbot",
        page_icon="☕",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Modern CSS for enhanced UI
    st.markdown("""
    <style>
    /* Global Variables */
    :root {
        --primary-color: #667eea;
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --dark-gradient: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        --glass-bg: rgba(255, 255, 255, 0.1);
        --glass-border: rgba(255, 255, 255, 0.2);
        --shadow-light: 0 8px 32px rgba(102, 126, 234, 0.1);
        --shadow-medium: 0 8px 32px rgba(102, 126, 234, 0.2);
        --shadow-heavy: 0 16px 48px rgba(102, 126, 234, 0.3);
        --border-radius: 16px;
        --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* Main App Styling */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }

    /* Sidebar Modern Styling */
    .css-1d391kg, .css-1cypcdb {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border-right: 1px solid var(--glass-border);
    }

    /* Header with Glass Morphism */
    .main-header {
        background: var(--primary-gradient);
        padding: 2rem;
        border-radius: var(--border-radius);
        margin-bottom: 2rem;
        box-shadow: var(--shadow-heavy);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        position: relative;
        overflow: hidden;
    }

    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: shimmer 3s ease-in-out infinite;
    }

    @keyframes shimmer {
        0%, 100% { transform: rotate(0deg); }
        50% { transform: rotate(180deg); }
    }

    .main-header h1 {
        color: white;
        text-align: center;
        margin: 0;
        font-weight: 700;
        font-size: 2.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }

    .main-header p {
        position: relative;
        z-index: 1;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }

    /* Response Container with Glass Effect */
    .response-container {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(20px);
        padding: 2rem;
        border-radius: var(--border-radius);
        border: 1px solid var(--glass-border);
        margin: 1.5rem 0;
        box-shadow: var(--shadow-medium);
        position: relative;
        overflow: hidden;
        transition: var(--transition);
    }

    .response-container:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-heavy);
    }

    .response-container::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        height: 100%;
        width: 4px;
        background: var(--primary-gradient);
        border-radius: 0 4px 4px 0;
    }

    /* User Message Styling */
    .user-message {
        background: var(--success-gradient);
        padding: 1.5rem;
        border-radius: var(--border-radius);
        margin: 1.5rem 0;
        box-shadow: var(--shadow-light);
        border: 1px solid var(--glass-border);
        position: relative;
        overflow: hidden;
    }

    .user-message strong {
        color: white;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }

    /* Code Block Modern Styling */
    .stCodeBlock {
        background: var(--dark-gradient) !important;
        border-radius: var(--border-radius) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: var(--shadow-medium) !important;
        margin: 1rem 0 !important;
    }

    /* Button Styling */
    .stButton > button {
        background: var(--primary-gradient);
        border: none;
        border-radius: var(--border-radius);
        padding: 0.75rem 1.5rem;
        color: white;
        font-weight: 600;
        box-shadow: var(--shadow-light);
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-heavy);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* Special Button Types */
    .stButton > button[data-testid*="clear"] {
        background: var(--secondary-gradient);
    }

    .stButton > button[data-testid*="save"] {
        background: var(--success-gradient);
    }

    /* Input Styling */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: var(--border-radius);
        padding: 1rem;
        transition: var(--transition);
    }

    .stTextArea textarea:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }

    /* Progress Bar Styling */
    .stProgress .st-bo {
        background: var(--primary-gradient);
        border-radius: 10px;
    }

    /* Sidebar Elements */
    .sidebar-section {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(20px);
        padding: 1.5rem;
        border-radius: var(--border-radius);
        margin-bottom: 1.5rem;
        border: 1px solid var(--glass-border);
        box-shadow: var(--shadow-light);
    }

    /* History Item Styling */
    .history-item {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 0.75rem;
        border: 1px solid var(--glass-border);
        box-shadow: var(--shadow-light);
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }

    .history-item::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        height: 100%;
        width: 3px;
        background: var(--primary-gradient);
        border-radius: 0 3px 3px 0;
    }

    .history-item:hover {
        transform: translateX(5px);
        box-shadow: var(--shadow-medium);
    }

    /* Toast/Alert Styling */
    .stAlert {
        border-radius: var(--border-radius);
        border: none;
        box-shadow: var(--shadow-light);
    }

    /* Success Messages */
    .stSuccess {
        background: var(--success-gradient);
        color: white;
    }

    /* Warning Messages */
    .stWarning {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        color: #8b4513;
    }

    /* Error Messages */
    .stError {
        background: var(--secondary-gradient);
        color: white;
    }

    /* Footer Styling */
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(20px);
        border-radius: var(--border-radius);
        border: 1px solid var(--glass-border);
        box-shadow: var(--shadow-light);
    }

    /* Metrics and Stats */
    .metric-card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(20px);
        padding: 1.5rem;
        border-radius: var(--border-radius);
        border: 1px solid var(--glass-border);
        box-shadow: var(--shadow-light);
        text-align: center;
        transition: var(--transition);
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: var(--shadow-heavy);
    }

    /* Copy Button Enhancement */
    .copy-button-modern {
        background: var(--primary-gradient);
        border: none;
        border-radius: 8px;
        padding: 8px 12px;
        color: white;
        cursor: pointer;
        transition: var(--transition);
        box-shadow: var(--shadow-light);
    }

    .copy-button-modern:hover {
        transform: scale(1.05);
        box-shadow: var(--shadow-medium);
    }

    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb {
        background: var(--primary-gradient);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-gradient);
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .response-container, .user-message {
            padding: 1rem;
        }
    }

    /* Loading Animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }

    .loading {
        animation: pulse 2s infinite;
    }

    /* Floating Action Style */
    .floating-element {
        position: relative;
        animation: float 3s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>☕ Java Expert Chatbot - Enterprise Ready</h1>
        <p style="color: white; text-align: center; margin: 0;">
            🔒 Security-First | 🏗️ MVC Architecture | 🚀 Production Ready | 💾 Auto-Save
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar with Modern Styling
    with st.sidebar:
        # Add sidebar header
        st.markdown("""
        <div style="background: var(--primary-gradient); padding: 1.5rem; border-radius: var(--border-radius); margin-bottom: 1.5rem; text-align: center; color: white; box-shadow: var(--shadow-medium);">
            <h2 style="margin: 0; font-size: 1.5rem; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">🎛️ Control Panel</h2>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 0.9rem;">Manage your Java learning journey</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Saved Histories Section
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
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: rgba(102, 126, 234, 0.1); border-radius: 12px; border: 2px dashed rgba(102, 126, 234, 0.3);">
                <div style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.6;">📚</div>
                <p style="color: var(--primary-color); font-weight: 600; margin: 0;">No saved histories yet</p>
                <p style="color: #666; font-size: 0.9rem; margin: 0.5rem 0 0 0;">Start a conversation to create your first history!</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Sample Questions Section
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
            # Create a custom styled button for each sample question
            st.markdown(f"""
            <div class="history-item" style="cursor: pointer; transition: var(--transition);" 
                 onmouseover="this.style.transform='translateX(8px) scale(1.02)'" 
                 onmouseout="this.style.transform='translateX(0) scale(1)'">
                <div style="font-weight: 600; color: var(--primary-color); margin-bottom: 0.25rem;">
                    💭 Sample #{i+1}
                </div>
                <div style="font-size: 0.9rem; line-height: 1.4;">
                    {question}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Initialize session state
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

    # Initialize the chatbot (streaming mode always enabled)
    try:
        # Try to get API key from secrets first, then from environment
        try:
            api_key = st.secrets["GROQ_API_KEY"]
        except:
            import os
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.getenv("GROQ_API_KEY")
            
        if not api_key:
            raise Exception("API key not found")
            
        chatbot = GroqJavaChatbot(api_key)
    except Exception as e:
        st.error("❌ API key not found. Please configure GROQ_API_KEY in Streamlit secrets or .env file.")
        st.stop()

    # Handle selected question from sidebar
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

    # Enhanced User Input Section
    st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(20px); 
                padding: 2rem; border-radius: var(--border-radius); 
                border: 1px solid var(--glass-border); box-shadow: var(--shadow-light); margin: 2rem 0;">
        <h3 style="color: var(--primary-color); margin: 0 0 1rem 0; font-weight: 700;">
            💭 Ask Your Java Question
        </h3>
        <p style="color: #666; margin: 0 0 1rem 0; font-size: 0.95rem;">
            Get expert advice on Java, Spring Boot, security, architecture, and best practices
        </p>
    </div>
    """, unsafe_allow_html=True)
    
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
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.6); backdrop-filter: blur(10px); 
                    padding: 1.5rem; border-radius: var(--border-radius); 
                    border: 1px solid var(--glass-border); box-shadow: var(--shadow-light); 
                    text-align: center; margin-top: 1rem;">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🎯</div>
            <div style="font-size: 0.85rem; color: var(--primary-color); font-weight: 600;">Action Center</div>
        </div>
        """, unsafe_allow_html=True)
        
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
    
    # Manual save chat history
    if save_button and st.session_state.chat_history and not st.session_state.current_chat_saved:
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
    
    # Clear chat history
    if clear_button:
        # Auto-save before clearing
        auto_save_current_chat()
        
        # Clear everything
        st.session_state.chat_history = []
        st.session_state.copied_code = {}
        st.session_state.current_query = ""
        st.session_state.current_chat_saved = False
        st.rerun()
    
    # Process user query
    if submit_button and st.session_state.current_query.strip():
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
        st.markdown(f"""
        <div class="user-message floating-element">
            <strong>👤 You:</strong><br>
            {st.session_state.current_query}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="response-container">
            <strong>🤖 Java Expert:</strong>
        </div>
        """, unsafe_allow_html=True)
        
        # Create streaming container
        streaming_container = st.empty()
        
        # Show modern progress with enhanced styling
        progress_container = st.container()
        with progress_container:
            st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(20px); 
                        padding: 1.5rem; border-radius: var(--border-radius); 
                        border: 1px solid var(--glass-border); box-shadow: var(--shadow-light); margin: 1rem 0;">
                <div style="text-align: center; margin-bottom: 1rem;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;" class="loading">🤖</div>
                    <div style="font-weight: 600; color: var(--primary-color);" id="status-text">Initializing AI...</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Custom streaming function with progress
        def stream_with_progress():
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
        
        # Get streaming response
        response = stream_with_progress()
        
        # Add bot response to history
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        # Clear the current query after processing
        st.session_state.current_query = ""
        
        # Rerun to show the new response in proper format
        st.rerun()
    
    elif submit_button and not st.session_state.current_query.strip():
        st.warning("⚠️ Please enter a question.")

    # Display chat history with enhanced styling
    if st.session_state.chat_history:
        # Show save status with modern design
        save_status_icon = "💾" if st.session_state.current_chat_saved else "⚠️"
        save_status_text = "Auto-saved" if st.session_state.current_chat_saved else "Not saved"
        save_status_color = "var(--success-gradient)" if st.session_state.current_chat_saved else "var(--secondary-gradient)"
        
        st.markdown(f"""
        <div style="background: {save_status_color}; padding: 1rem 1.5rem; border-radius: var(--border-radius); 
                    margin: 2rem 0 1rem 0; color: white; box-shadow: var(--shadow-light);">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="font-size: 1.5rem;">{save_status_icon}</span>
                    <span style="font-weight: 700; font-size: 1.2rem;">💬 Chat History</span>
                </div>
                <div style="background: rgba(255, 255, 255, 0.2); padding: 0.5rem 1rem; 
                           border-radius: 20px; font-size: 0.9rem; font-weight: 600;">
                    {save_status_text}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        for i, message in enumerate(st.session_state.chat_history):
            if message["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    <strong>👤 You:</strong><br>
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            
            else:  # assistant
                st.markdown("""
                <div class="response-container">
                    <strong>🤖 Java Expert:</strong>
                </div>
                """, unsafe_allow_html=True)
                
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
                        st.subheader(f"📄 Code Example {j+1}" + (f" ({language})" if language else ""))
                        
                        # Create columns for code and copy button
                        code_col, copy_col = st.columns([10, 1])
                        
                        with code_col:
                            st.code(code, language=language if language else 'java')
                        
                        with copy_col:
                            copy_key = f"copy_{i}_{j}"
                            if st.button("📋", key=copy_key, help="Copy code"):
                                # Store the code in session state for copying
                                st.session_state.copied_code[copy_key] = code
                                st.success("✅ Copied!")
                                
                                # JavaScript to copy to clipboard
                                code_json = json.dumps(code)
                                st.components.v1.html(f"""
                                <script>
                                    navigator.clipboard.writeText({code_json}).then(function() {{
                                        console.log('Code copied to clipboard');
                                    }});
                                </script>
                                """, height=0)
                else:
                    # No code blocks, display normally
                    st.markdown(response_content)
                
                st.markdown("---")

    # Modern Footer with Enhanced Styling
    st.markdown("""
    <div class="footer floating-element">
        <div style="display: flex; justify-content: center; align-items: center; flex-wrap: wrap; gap: 2rem; margin-bottom: 1rem;">
            <div class="metric-card" style="min-width: 150px;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎯</div>
                <div style="font-weight: 600; color: var(--primary-color);">Enterprise Ready</div>
            </div>
            <div class="metric-card" style="min-width: 150px;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔒</div>
                <div style="font-weight: 600; color: var(--primary-color);">Security First</div>
            </div>
            <div class="metric-card" style="min-width: 150px;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🚀</div>
                <div style="font-weight: 600; color: var(--primary-color);">Production Ready</div>
            </div>
            <div class="metric-card" style="min-width: 150px;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">💾</div>
                <div style="font-weight: 600; color: var(--primary-color);">Auto-Save</div>
            </div>
        </div>
        <div style="background: var(--primary-gradient); padding: 1rem; border-radius: 12px; color: white; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">
            <p style="margin: 0; font-weight: 600; font-size: 1.1rem;">🎯 Enterprise Java Development Assistant</p>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Powered by Groq API | Advanced AI | Modern UI</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()