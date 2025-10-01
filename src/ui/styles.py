"""
CSS Styles for the Java Expert Chatbot Application
"""

import streamlit as st

def load_styles():
    """Load all CSS styles for the application"""
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