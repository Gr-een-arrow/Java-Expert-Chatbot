"""
UI Components for the Java Expert Chatbot Application
"""

import streamlit as st
import json

def render_header():
    """Render the main header section"""
    st.markdown("""
    <div class="main-header">
        <h1>☕ Java Expert Chatbot - Enterprise Ready</h1>
        <p style="color: white; text-align: center; margin: 0;">
            🔒 Security-First | 🏗️ MVC Architecture | 🚀 Production Ready | 💾 Auto-Save
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_user_input_section():
    """Render the user input section"""
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

def render_action_center():
    """Render the action center panel"""
    st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.6); backdrop-filter: blur(10px); 
                padding: 1.5rem; border-radius: var(--border-radius); 
                border: 1px solid var(--glass-border); box-shadow: var(--shadow-light); 
                text-align: center; margin-top: 1rem;">
        <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🎯</div>
        <div style="font-size: 0.85rem; color: var(--primary-color); font-weight: 600;">Action Center</div>
    </div>
    """, unsafe_allow_html=True)

def render_user_message(content):
    """Render a user message"""
    st.markdown(f"""
    <div class="user-message floating-element">
        <strong>👤 You:</strong><br>
        {content}
    </div>
    """, unsafe_allow_html=True)

def render_assistant_response_header():
    """Render the assistant response header"""
    st.markdown("""
    <div class="response-container">
        <strong>🤖 Java Expert:</strong>
    </div>
    """, unsafe_allow_html=True)

def render_loading_indicator():
    """Render loading indicator with progress"""
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

def render_chat_history_header(is_saved):
    """Render chat history section header"""
    save_status_icon = "💾" if is_saved else "⚠️"
    save_status_text = "Auto-saved" if is_saved else "Not saved"
    save_status_color = "var(--success-gradient)" if is_saved else "var(--secondary-gradient)"
    
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

def render_code_block_with_copy(code, language, message_index, block_index):
    """Render a code block with copy functionality"""
    st.subheader(f"📄 Code Example {block_index + 1}" + (f" ({language})" if language else ""))
    
    # Create columns for code and copy button
    code_col, copy_col = st.columns([10, 1])
    
    with code_col:
        st.code(code, language=language if language else 'java')
    
    with copy_col:
        copy_key = f"copy_{message_index}_{block_index}"
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

def render_footer():
    """Render the application footer"""
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

def render_empty_history_state():
    """Render empty state for history section"""
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: rgba(102, 126, 234, 0.1); border-radius: 12px; border: 2px dashed rgba(102, 126, 234, 0.3);">
        <div style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.6;">📚</div>
        <p style="color: var(--primary-color); font-weight: 600; margin: 0;">No saved histories yet</p>
        <p style="color: #666; font-size: 0.9rem; margin: 0.5rem 0 0 0;">Start a conversation to create your first history!</p>
    </div>
    """, unsafe_allow_html=True)

def render_sample_question_item(question, index):
    """Render a sample question item"""
    st.markdown(f"""
    <div class="history-item" style="cursor: pointer; transition: var(--transition);" 
         onmouseover="this.style.transform='translateX(8px) scale(1.02)'" 
         onmouseout="this.style.transform='translateX(0) scale(1)'">
        <div style="font-weight: 600; color: var(--primary-color); margin-bottom: 0.25rem;">
            💭 Sample #{index + 1}
        </div>
        <div style="font-size: 0.9rem; line-height: 1.4;">
            {question}
        </div>
    </div>
    """, unsafe_allow_html=True)