import streamlit as st
from chat import JavaChatbot

def main():
    st.set_page_config(
        page_title="Java Expert Chatbot",
        page_icon="☕",
        layout="wide"
    )
    
    # Header
    st.title("☕ Java Expert Chatbot")
    st.markdown("Get expert advice on Java, Spring Boot, security, and best practices")
    
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
    
    # User input
    user_query = st.text_area("Your Java Question:", height=100, 
                             placeholder="Example: How to implement JWT authentication in Spring Boot?")
    
    if st.button("Ask Expert", type="primary"):
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