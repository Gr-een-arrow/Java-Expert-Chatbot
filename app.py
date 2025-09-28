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
        layout="wide"
    )
    
    # Header
    st.title("☕ Java Expert Chatbot")
    st.markdown("Get expert advice on Java, Spring Boot, security, and best practices")
    
    # Sidebar for saved histories
    with st.sidebar:
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
            st.info("No saved histories yet. Start a conversation to create your first history!")
    
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
    
    # User input and controls
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_query = st.text_area("Your Java Question:", height=100, 
                                 placeholder="Example: How to implement JWT authentication in Spring Boot?")
    
    with col2:
        st.write("")  # Spacing
        ask_button = st.button("🚀 Ask Expert", type="primary", use_container_width=True)
        
        col2a, col2b = st.columns(2)
        with col2a:
            clear_button = st.button("🗑️ Clear", use_container_width=True)
        with col2b:
            save_button = st.button("💾 Save", use_container_width=True, 
                                   disabled=len(st.session_state.chat_history) == 0)
    
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
    
    # Display chat history
    if st.session_state.chat_history:
        st.subheader("Chat History")
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"**👤 You:** {message['content']}")
            else:
                st.markdown(f"**🤖 Java Expert:** {message['content']}")
            st.markdown("---")

if __name__ == "__main__":
    main()