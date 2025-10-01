"""
Configuration file for the Java Expert Chatbot Application
"""

# Application Settings
APP_CONFIG = {
    "page_title": "Java Expert Chatbot",
    "page_icon": "☕",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# UI Settings
UI_CONFIG = {
    "header_title": "☕ Java Expert Chatbot - Enterprise Ready",
    "header_subtitle": "🔒 Security-First | 🏗️ MVC Architecture | 🚀 Production Ready | 💾 Auto-Save",
    "sidebar_title": "🎛️ Control Panel", 
    "sidebar_subtitle": "Manage your Java learning journey",
    "footer_title": "🎯 Enterprise Java Development Assistant",
    "footer_subtitle": "Powered by Groq API | Advanced AI | Modern UI"
}

# Sample Questions
SAMPLE_QUESTIONS = [
    "How to implement pagination in Spring Boot?",
    "Create a secure REST API with JWT authentication",
    "How to use MapStruct for entity-DTO mapping?",
    "Implement global exception handling in Spring Boot",
    "Create a complete CRUD operation with security",
    "How to implement audit trail in Spring Boot?",
    "Best practices for Spring Boot validation"
]

# File Settings
FILE_CONFIG = {
    "history_dir": "chat_history",
    "max_filename_length": 50,
    "max_histories_display": 10,
    "max_display_name_length": 32
}

# UI Text
UI_TEXT = {
    "input_placeholder": "🚀 Example: How to implement JWT authentication in Spring Boot?\n💡 Or: Best practices for RESTful API design?\n🔒 Or: How to secure a Spring Boot application?",
    "no_histories_message": "No saved histories yet",
    "no_histories_subtitle": "Start a conversation to create your first history!",
    "api_error_message": "❌ API key not found. Please configure GROQ_API_KEY in Streamlit secrets or .env file.",
    "empty_question_warning": "⚠️ Please enter a question.",
    "history_loaded_success": "✅ History loaded!",
    "history_deleted_success": "✅ Deleted!",
    "history_updated_success": "✅ Name updated!",
    "history_saved_success": "✅ History saved as: {filename}",
    "code_copied_success": "✅ Copied!",
    "auto_save_message": "💾 Previous chat auto-saved: {filename}..."
}

# Progress Messages
PROGRESS_MESSAGES = [
    "🔍 Analyzing your question...",
    "🧠 Generating enterprise-grade solution...",
    "🔒 Adding security best practices...",
    "📝 Creating complete code examples...",
    "✅ Response completed!"
]

# Progress Steps (percentages)
PROGRESS_STEPS = [10, 30, 50, 70, 100]