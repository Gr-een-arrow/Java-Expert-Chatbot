import streamlit as st
import re
import json
import os
from datetime import datetime
from chat import JavaChatbot

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
                            "question": data.get("question", "Unknown Question"),
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
        --glass-bg: rgba(255, 255, 255, 0.1);
        --glass-border: rgba(255, 255, 255, 0.2);
        --shadow-light: 0 8px 32px rgba(102, 126, 234, 0.1);
        --shadow-medium: 0 8px 32px rgba(102, 126, 234, 0.2);
        --border-radius: 16px;
        --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* Main App Styling */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }

    /* Header with Glass Morphism */
    .main-header {
        background: var(--primary-gradient);
        padding: 2rem;
        border-radius: var(--border-radius);
        margin-bottom: 2rem;
        box-shadow: var(--shadow-medium);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        position: relative;
        overflow: hidden;
    }

    .main-header h1 {
        color: white;
        text-align: center;
        margin: 0;
        font-weight: 700;
        font-size: 2.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
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
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-medium);
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

    /* User Message Styling */
    .user-message {
        background: var(--success-gradient);
        padding: 1.5rem;
        border-radius: var(--border-radius);
        margin: 1.5rem 0;
        box-shadow: var(--shadow-light);
        border: 1px solid var(--glass-border);
    }

    .user-message strong {
        color: white;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }

    /* Response Container */
    .response-container {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(20px);
        padding: 2rem;
        border-radius: var(--border-radius);
        border: 1px solid var(--glass-border);
        margin: 1.5rem 0;
        box-shadow: var(--shadow-medium);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>☕ Java Expert Chatbot - Enterprise Ready</h1>
        <p style="color: white; text-align: center; margin: 0;">
            🔒 Security-First | 🏗️ MVC Architecture | 🚀 Production Ready
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
                display_text = history["question"][:30] + "..." if len(history["question"]) > 30 else history["question"]
                if st.button(f"📄 {display_text}", key=f"load_history_{i}"):
                    st.session_state.chat_history = history["chat_history"]
                    st.success("✅ History loaded!")
                    st.rerun()
        else:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: rgba(102, 126, 234, 0.1); border-radius: 12px; border: 2px dashed rgba(102, 126, 234, 0.3);">
                <div style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.6;">📚</div>
                <p style="color: var(--primary-color); font-weight: 600; margin: 0;">No saved histories yet</p>
                <p style="color: #666; font-size: 0.9rem; margin: 0.5rem 0 0 0;">Start a conversation to create your first history!</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Initialize session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Initialize chatbot
    try:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            st.error("❌ API key not found. Please configure GROQ_API_KEY in .env file.")
            st.stop()
            
        chatbot = JavaChatbot(api_key)
    except Exception as e:
        st.error(f"❌ Error initializing chatbot: {e}")
        st.stop()
    
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
            height=120,
            placeholder="🚀 Example: How to implement JWT authentication in Spring Boot?\n💡 Or: Best practices for RESTful API design?\n🔒 Or: How to secure a Spring Boot application?",
            label_visibility="collapsed"
        )
    
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
        ask_button = st.button("🚀 Ask Expert", type="primary", use_container_width=True)
        
        st.markdown('<div style="margin-top: 1rem;">', unsafe_allow_html=True)
        col2a, col2b = st.columns(2)
        with col2a:
            clear_button = st.button("🗑️ Clear", use_container_width=True)
        with col2b:
            save_button = st.button("💾 Save", use_container_width=True, 
                                   disabled=len(st.session_state.chat_history) == 0)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle buttons
    if ask_button:
        if user_query.strip():
            # Add user message
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            
            # Get bot response
            with st.spinner("Generating response..."):
                response = chatbot.get_response(user_query)
            
            # Add bot response
            st.session_state.chat_history.append({"role": "assistant", "content": response})
        else:
            st.warning("Please enter a question.")
    
    # Clear chat history
    if clear_button:
        st.session_state.chat_history = []
        st.rerun()
    
    # Save chat history
    if save_button and st.session_state.chat_history:
        # Get the first user question as the history name
        first_question = None
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                first_question = message["content"]
                break
        
        if first_question:
            saved_file = save_chat_history(first_question, st.session_state.chat_history)
            if saved_file:
                st.success(f"✅ History saved!")
                st.rerun()
        else:
            st.warning("⚠️ No questions found in chat history.")
    
    # Display chat history with enhanced styling
    if st.session_state.chat_history:
        st.markdown("""
        <div style="background: var(--success-gradient); padding: 1rem 1.5rem; border-radius: var(--border-radius); 
                    margin: 2rem 0 1rem 0; color: white; box-shadow: var(--shadow-light);">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.5rem;">💬</span>
                <span style="font-weight: 700; font-size: 1.2rem;">Chat History</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    <strong>👤 You:</strong><br>
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="response-container">
                    <strong>🤖 Java Expert:</strong>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(message["content"])
                st.markdown("---")

if __name__ == "__main__":
    main()