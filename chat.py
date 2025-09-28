import requests
import json
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

class JavaChatbot:
    def __init__(self, api_key: str):
        """
        Initialize the Java Chatbot with Groq API key
        """
        self.api_key = api_key
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.conversation_history = []
        
        # Define knowledge base for Java topics
        self.java_topics = {
            "core_java": [
                "variables", "data types", "operators", "control structures",
                "loops", "arrays", "methods", "classes", "objects", "inheritance",
                "polymorphism", "encapsulation", "abstraction", "interfaces",
                "exceptions", "collections", "generics", "threads", "lambda expressions"
            ],
            "spring_boot": [
                "annotations", "dependency injection", "rest controllers", "jpa",
                "hibernate", "configuration", "profiles", "actuator", "security",
                "testing", "microservices", "data access", "web mvc"
            ]
        }

    def create_system_prompt(self) -> str:
        return """
        You are a highly skilled Java and Spring Boot mentor.
        Your task is to generate clear, structured, and enterprise-grade explanations 
        for any question about Java, Core Java, or Spring Boot.

        Follow this response structure:
        1. Concept Explanation - Simple, beginner-friendly terms
        2. Security Considerations - Enterprise security practices
        3. Code Example - Complete, runnable examples with proper structure
        4. Best Practices - Modern Java/Spring Boot recommendations
        5. Common Mistakes - What to avoid and why
        
        Requirements:
        - Always prioritize security best practices
        - Use proper MVC architecture separation
        - Provide complete, production-ready code
        - Include proper error handling
        - Follow enterprise coding standards
        """

    def detect_java_topic(self, query: str) -> str:
        query_lower = query.lower()
        
        spring_keywords = [
            "spring", "boot", "annotation", "controller", "service", "repository",
            "autowired", "component", "restcontroller", "requestmapping",
            "jpa", "hibernate", "entity", "configuration", "profile", "security"
        ]
        
        core_keywords = [
            "class", "object", "inheritance", "polymorphism", "interface",
            "abstract", "exception", "collection", "arraylist", "hashmap",
            "thread", "lambda", "stream", "generic", "enum"
        ]
        
        spring_matches = sum(1 for keyword in spring_keywords if keyword in query_lower)
        core_matches = sum(1 for keyword in core_keywords if keyword in query_lower)
        
        return "spring_boot" if spring_matches > core_matches else "core_java"
    
    def enhance_prompt_with_context(self, user_query: str) -> str:
        topic = self.detect_java_topic(user_query)
        
        context = f"""
        User Query: {user_query}
        
        Detected Topic: {topic.replace('_', ' ').title()}
        
        Please provide a comprehensive response following the structured format:
        - Concept Explanation
        - Security Considerations  
        - Complete Code Example
        - Best Practices
        - Common Mistakes to Avoid
        """
        
        return context
    
    def get_response(self, user_query: str) -> str:
        try:
            enhanced_query = self.enhance_prompt_with_context(user_query)
            self.conversation_history.append({"role": "user", "content": enhanced_query})
            
            # Keep conversation history manageable
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            messages = [
                {"role": "system", "content": self.create_system_prompt()}
            ] + self.conversation_history
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "moonshotai/kimi-k2-instruct",
                "messages": messages,
                "max_tokens": 4000,
                "temperature": 0.1,
                "top_p": 0.9,
                "stream": False
            }
            
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                response_data = response.json()
                bot_response = response_data['choices'][0]['message']['content']
                self.conversation_history.append({"role": "assistant", "content": bot_response})
                return bot_response
            else:
                return f"API Error: {response.status_code} - {response.text}"
            
        except requests.exceptions.RequestException as e:
            return f"Network error: {str(e)}. Please check your internet connection."
        except json.JSONDecodeError as e:
            return f"JSON parsing error: {str(e)}. Please try again."
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}. Please try rephrasing your question."

def load_api_key():
    """Load API key from environment variables"""
    load_dotenv()
    
    api_key = os.getenv('GROQ_API_KEY')
    
    if not api_key:
        print("❌ GROQ_API_KEY not found in environment variables!")
        print("\n🔧 Setup Instructions:")
        print("1. Create a .env file in the same directory as this script")
        print("2. Add the following line to the .env file:")
        print("   GROQ_API_KEY=your_actual_api_key_here")
        print("3. Save the file and restart the application")
        return None
    
    return api_key

def main():
    """Main function to run the chatbot in terminal mode"""
    print("🚀 Java Expert Chatbot - Security & MVC Focused")
    print("=" * 50)
    
    api_key = load_api_key()
    if not api_key:
        return
    
    print("✅ API key loaded successfully!")
    print("🔒 Specialized in secure, production-ready Java solutions!")
    print("Type 'exit' to quit")
    print("=" * 50)
    
    chatbot = JavaChatbot(api_key)
    
    while True:
        user_input = input("\n💭 Your Question: ").strip()
        
        if user_input.lower() == 'exit':
            print("👋 Goodbye! Keep coding securely!")
            break
        
        if not user_input:
            print("❌ Please enter a valid question.")
            continue
        
        print("\n🤖 Expert Response:")
        print("-" * 30)
        response = chatbot.get_response(user_input)
        print(response)
        print("-" * 30)

if __name__ == "__main__":
    main()