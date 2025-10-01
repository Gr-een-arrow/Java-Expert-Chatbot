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

        Follow this response structure every time:

        🤖 Secure & MVC-Compliant Response:
        -------------------------------------
        # Concept Explanation
        - Explain the concept in simple, beginner-friendly terms.
        - Use short examples where necessary.

        # Security Considerations
        - Explain how the concept should be applied securely in enterprise systems.
        - Cover validation, data protection, authentication, and safe coding practices.

        # Full Code Example (Enterprise Package Structure)
        - Provide a runnable Spring Boot example with correct package structure.
        - Include DTOs, Service, Repository, Controller, Config, Exception handling.
        - Ensure the code follows SOLID principles and is security-aware.
        - Always show `application.yml` for relevant configs.

        # Step-by-Step Explanation
        - Walk through how each part of the code works and why it's important.

        # Best Practices & Performance Tips
        - List modern Java + Spring Boot best practices.
        - Emphasize secure, scalable, and maintainable design.

        # Common Mistakes to Avoid
        - Show common pitfalls and why they should be avoided.

        # Related Concepts
        - Provide links to related Java/Spring Boot topics (conceptual references).

        # Testing Example
        - Provide JUnit/MockMvc/DataJpaTest snippets to validate correctness.

        # Summary
        - End with a short recap of what was explained.

        MANDATORY REQUIREMENTS:

        1. SECURITY FIRST:
        - Always validate inputs (Bean Validation, regex, sanitization).
        - Use strong password handling (BCrypt, never plain text).
        - Prevent SQL Injection (use JPA, parameterized queries).
        - Implement CSRF protection in web apps.
        - Apply authentication & authorization (JWT/OAuth2/Role-based).
        - Never expose sensitive data in logs or responses.
        - Include audit logging for critical events.

        2. MVC ARCHITECTURE COMPLIANCE:
        - Model: Entities with JPA + validation annotations.
        - DTOs: Separate request/response models (never expose entities directly).
        - Repository: Data access only.
        - Service: Business logic with @Transactional.
        - Controller: REST endpoints, validation, proper HTTP status codes.
        - Configuration: Proper use of application.yml and profiles.

        3. ENTERPRISE STANDARDS:
        - Use Java conventions, SOLID principles, and design patterns.
        - Include logging, exception handling, and comprehensive testing.
        - Show proper equals(), hashCode(), and builder patterns where needed.
        - Provide complete runnable code with package structure and imports.
        - Use correct annotations (@RestController, @Service, @Repository).
        - Show dependency injection with constructor injection (preferred).
        - Include actuator monitoring and transaction management.

        4. ADVANCED ENTERPRISE PATTERNS (MANDATORY):
        
        A. DTO ↔ Entity Mapping:
        - NEVER use manual mapping in services (avoid repetitive mapping code)
        - ALWAYS use MapStruct for type-safe, compile-time mapping
        - Show @Mapper interfaces with @Mapping annotations
        - Include mapping for nested objects and collections
        - Demonstrate bidirectional mapping (Entity→DTO and DTO→Entity)
        
        B. Structured Error Responses:
        - NEVER return raw strings from GlobalExceptionHandler
        - ALWAYS return structured JSON with consistent format
        - Include: {"error": "message", "code": "ERROR_CODE", "timestamp": "...", "path": "...}
        - Show proper HTTP status codes for different error types
        - Include validation error details with field-specific messages
        
        C. Complete Security Implementation:
        - ALWAYS include JwtAuthenticationFilter implementation
        - Show complete JWT token validation and parsing
        - Include proper exception handling in security filters
        - Demonstrate SecurityContext population with user details
        
        D. Audit Trail Implementation:
        - ALWAYS implement AuditorAware<String> for audit fields
        - Show integration with JWT to extract current user for created_by/updated_by
        - Include @EnableJpaAuditing configuration
        - Demonstrate audit fields in base entities (createdBy, lastModifiedBy)

        5. CODE QUALITY REQUIREMENTS:
        - MapStruct mapping interfaces for all DTO conversions
        - Structured error response DTOs with consistent format
        - Complete JWT filter implementation with proper error handling
        - AuditorAware implementation extracting user from SecurityContext
        - Comprehensive validation with custom error messages
        - Proper transaction boundaries and rollback scenarios
        - Performance optimizations (pagination, projections, caching)

        6. COMPLETENESS REQUIREMENT:
        - Never truncate or give partial code.
        - Always provide working, runnable examples.
        - Include ALL necessary methods, classes, and configurations.
        - Show full configuration files when relevant.
        - Provide comprehensive test examples.
        - Include MapStruct configuration and dependencies.
        - Show complete security filter chain configuration.
        - Demonstrate audit configuration and implementation.

        EXAMPLES TO ALWAYS INCLUDE:

        ```java
        // MapStruct Mapper Example
        @Mapper(componentModel = "spring", unmappedTargetPolicy = ReportingPolicy.IGNORE)
        public interface ProductMapper {
            ProductResponseDto toDto(Product product);
            Product toEntity(ProductRequestDto dto);
            @Mapping(target = "id", ignore = true)
            @Mapping(target = "createdAt", ignore = true)
            Product toEntityForCreate(ProductRequestDto dto);
        }

        // Structured Error Response Example
        @Data
        @Builder
        public class ErrorResponse {
            private String error;
            private String code;
            private LocalDateTime timestamp;
            private String path;
            private Map<String, String> validationErrors;
        }

        // JWT Filter Implementation Example
        @Component
        public class JwtAuthenticationFilter extends OncePerRequestFilter {
            // Complete implementation with error handling
        }

        // AuditorAware Implementation Example
        @Component
        public class AuditorAwareImpl implements AuditorAware<String> {
            @Override
            public Optional<String> getCurrentAuditor() {
                Authentication auth = SecurityContextHolder.getContext().getAuthentication();
                return Optional.ofNullable(auth)
                    .filter(Authentication::isAuthenticated)
                    .map(Authentication::getName);
            }
        }
        """

    def detect_java_topic(self, query: str) -> str:
        query_lower = query.lower()
        
        spring_keywords = [
            "spring", "boot", "annotation", "controller", "service", "repository",
            "autowired", "component", "restcontroller", "requestmapping",
            "jpa", "hibernate", "entity", "configuration", "profile", "security",
            "authentication", "authorization", "jwt", "oauth", "rest", "api"
        ]
        
        core_keywords = [
            "class", "object", "inheritance", "polymorphism", "interface",
            "abstract", "exception", "collection", "arraylist", "hashmap",
            "thread", "lambda", "stream", "generic", "enum", "serialization"
        ]
        
        spring_matches = sum(1 for keyword in spring_keywords if keyword in query_lower)
        core_matches = sum(1 for keyword in core_keywords if keyword in query_lower)
        
        if spring_matches > core_matches:
            return "spring_boot"
        else:
            return "core_java"
    
    def enhance_prompt_with_context(self, user_query: str) -> str:
        topic = self.detect_java_topic(user_query)
        
        context = f"""
        User Query: {user_query}
        
        Detected Topic: {topic.replace('_', ' ').title()}
        
        MANDATORY REQUIREMENTS for your response:
        
        1. SECURITY REQUIREMENTS:
        - Include proper input validation (Bean Validation annotations)
        - Show secure password handling (BCrypt encoding)
        - Implement proper exception handling
        - Include CSRF protection if web-related
        - Show SQL injection prevention
        - Include proper authentication/authorization if applicable
        - Never expose sensitive data
        - Add audit logging for security events
        
        2. MVC ARCHITECTURE REQUIREMENTS:
        - Model: Entities with JPA annotations, validation, audit fields
        - View: Separate DTOs for requests/responses
        - Controller: HTTP handling, validation, proper status codes
        - Service: Business logic with @Transactional
        - Repository: Data access with proper query methods
        - Show complete layer separation
        
        3. ENTERPRISE PATTERNS (CRITICAL):
        
        A. DTO Mapping Requirements:
        - MUST use MapStruct for all Entity ↔ DTO conversions
        - NEVER write manual mapping code in services
        - Show @Mapper interface with proper annotations
        - Include bidirectional mapping methods
        - Demonstrate nested object mapping
        
        B. Error Response Requirements:
        - MUST return structured JSON error responses
        - NEVER return raw strings from exception handlers
        - Include error code, message, timestamp, and path
        - Show validation error handling with field details
        - Use consistent error response format across all endpoints
        
        C. Security Implementation Requirements:
        - MUST include complete JwtAuthenticationFilter implementation
        - Show JWT token parsing and validation logic
        - Include proper security exception handling
        - Demonstrate SecurityContext population
        
        D. Audit Trail Requirements:
        - MUST implement AuditorAware<String> for audit fields
        - Show integration with JWT to extract current user
        - Include @EnableJpaAuditing configuration
        - Demonstrate createdBy/lastModifiedBy field population
        
        4. CODE QUALITY REQUIREMENTS:
        - Include all necessary imports and annotations
        - Show proper package structure
        - Add comprehensive error handling
        - Include logging statements
        - Follow Java naming conventions
        - Use appropriate design patterns
        - Show configuration examples (application.yml)
        - Include MapStruct dependency configuration
        
        5. PROVIDE COMPLETE EXAMPLES:
        - Entity classes with audit fields
        - MapStruct mapper interfaces
        - Structured error response DTOs
        - Complete JWT filter implementation
        - AuditorAware implementation
        - Repository interfaces
        - Service classes using MapStruct
        - Controller classes with proper error handling
        - Configuration classes
        - Unit test examples
        
        6. COMPLETENESS REQUIREMENT:
        - Provide COMPLETE implementations without truncation
        - Include all necessary methods and classes
        - Show full configuration files (pom.xml, application.yml)
        - Provide working, runnable code examples
        - Include MapStruct configuration and usage
        - Show complete security filter chain setup
        - Demonstrate audit configuration
        
        Make sure your response is production-ready and follows enterprise-level standards.
        Include everything needed to implement the solution completely with MapStruct, 
        structured error responses, complete JWT implementation, and audit trail.
        """
        
        return context
    
    def get_response(self, user_query: str) -> str:
        try:
            enhanced_query = self.enhance_prompt_with_context(user_query)
            self.conversation_history.append({"role": "user", "content": enhanced_query})
            
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
                "max_tokens": 8000,
                "temperature": 0.1,
                "top_p": 0.9,
                "stream": False
            }
            
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=90
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
    
    def get_sample_questions(self) -> Dict[str, List[str]]:
        return {
            "Core Java Security & Best Practices": [
                "How to implement secure password validation in Java?",
                "What are the best practices for exception handling in Java?",
                "How to prevent SQL injection in Java applications?",
                "How to implement proper input validation using Bean Validation?",
                "How to handle sensitive data securely in Java?",
                "What are the security considerations for Java collections?",
                "How to implement secure file handling in Java?"
            ],
            "Spring Boot Security & MVC": [
                "How to implement complete user authentication with proper MVC architecture?",
                "How to create secure REST APIs with input validation in Spring Boot?",
                "How to implement role-based authorization following MVC principles?",
                "How to secure database operations and prevent SQL injection in Spring Boot?",
                "How to implement proper exception handling across all MVC layers?",
                "How to create secure file upload functionality in Spring Boot?",
                "How to implement CORS security in Spring Boot applications?",
                "How to structure a Spring Boot application following MVC architecture?",
                "How to implement proper logging and monitoring in Spring Boot?",
                "How to create comprehensive unit tests for all MVC layers?"
            ]
        }

class GroqJavaChatbot:
    """Alternative implementation with streaming support and enhanced prompting"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        
    def stream_response(self, user_query: str, print_to_terminal: bool = True, streamlit_container=None):
        """Stream response from API with enhanced system prompt"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        enhanced_system_prompt = """
        You are a highly skilled Java and Spring Boot mentor. 
        Your task is to generate clear, structured, and enterprise-grade explanations 
        for any question about Java, Core Java, or Spring Boot.

        Follow this response structure every time:

        🤖 Secure & MVC-Compliant Response:
        -------------------------------------
        # Concept Explanation
        - Explain the concept in simple, beginner-friendly terms.
        - Use short examples where necessary.

        # Security Considerations
        - Explain how the concept should be applied securely in enterprise systems.
        - Cover validation, data protection, authentication, and safe coding practices.

        # Full Code Example (Enterprise Package Structure)
        - Provide a runnable Spring Boot example with correct package structure.
        - Include DTOs, Service, Repository, Controller, Config, Exception handling.
        - Ensure the code follows SOLID principles and is security-aware.
        - Always show `application.yml` for relevant configs.

        # Step-by-Step Explanation
        - Walk through how each part of the code works and why it's important.

        # Best Practices & Performance Tips
        - List modern Java + Spring Boot best practices.
        - Emphasize secure, scalable, and maintainable design.

        # Common Mistakes to Avoid
        - Show common pitfalls and why they should be avoided.

        # Related Concepts
        - Provide links to related Java/Spring Boot topics (conceptual references).

        # Testing Example
        - Provide JUnit/MockMvc/DataJpaTest snippets to validate correctness.

        # Summary
        - End with a short recap of what was explained.

        REQUIREMENTS:
        - Apply security best practices (validation, BCrypt, SQL injection prevention, CSRF, auth).
        - Use full MVC separation (Entity, DTO, Repository, Service, Controller).
        - Provide runnable, production-ready code with imports, configuration, and tests.
        - Include explanations, best practices, and pitfalls to avoid.
        - Never truncate responses. Always provide complete code and explanations.
        - Ensure solutions follow enterprise-grade standards.
        - ALWAYS use MapStruct for DTO mapping.
        - ALWAYS return structured JSON error responses.
        - ALWAYS include complete JWT filter implementation.
        - ALWAYS implement AuditorAware for audit trails.

        Tone: Professional, structured, and concise. Always prioritize security and enterprise-readiness.
        """

        payload = {
            "model": "moonshotai/kimi-k2-instruct",
            "messages": [
                {"role": "system", "content": enhanced_system_prompt},
                {"role": "user", "content": f"""
                {user_query}
                
                Please provide a complete response following the structured format:
                - Concept Explanation
                - Security Considerations
                - Full Code Example with Enterprise Package Structure
                - Step-by-Step Explanation
                - Best Practices & Performance Tips
                - Common Mistakes to Avoid
                - Related Concepts
                - Testing Example
                - Summary
                
                IMPORTANT: Use the full token limit to provide COMPLETE implementations.
                Include ALL necessary code without truncation.
                Use MapStruct for mapping, structured error responses, complete JWT filters, and audit implementation.
                """}
            ],
            "max_tokens": 8000,
            "temperature": 0.1,
            "stream": True
        }
        
        try:
            if print_to_terminal:
                print(f"\n🤖 Generating response for: {user_query}")
                print("=" * 80)
            
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                stream=True,
                timeout=45
            )
            
            if response.status_code == 200:
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith('data: '):
                            data = line[6:]
                            if data.strip() == '[DONE]':
                                break
                            try:
                                json_data = json.loads(data)
                                if 'choices' in json_data and len(json_data['choices']) > 0:
                                    delta = json_data['choices'][0].get('delta', {})
                                    if 'content' in delta:
                                        content = delta['content']
                                        if print_to_terminal:
                                            print(content, end='', flush=True)  # Terminal streaming
                                        
                                        full_response += content
                                        
                                        # ✅ Streamlit UI streaming
                                        if streamlit_container:
                                            streamlit_container.markdown(full_response)
                                        
                            except json.JSONDecodeError:
                                continue
                
                if print_to_terminal:
                    print("\n" + "=" * 80)
                    print("✅ Response completed!")
                
                return full_response
            else:
                error_msg = f"API Error: {response.status_code} - {response.text}"
                if print_to_terminal:
                    print(f"❌ {error_msg}")
                return error_msg
                 
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            if print_to_terminal:
                print(f"❌ {error_msg}")
            return error_msg

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
        print("\n📝 To get your API key:")
        print("   - Visit: https://console.groq.com/")
        print("   - Sign up/login and go to API Keys section")
        print("   - Create a new API key and copy it")
        return None
    
    return api_key

def main():
    """Main function to run the chatbot"""
    print("🚀 Java Expert Chatbot - Security & MVC Focused (Powered by Groq)")
    print("=" * 60)
    
    api_key = load_api_key()
    if not api_key:
        return
    
    print("✅ API key loaded successfully!")
    print("🔒 I specialize in secure, production-ready Java and Spring Boot solutions!")
    print("🏗️  All responses follow proper MVC architecture and security best practices!")
    print("Type 'exit' to quit, 'samples' to see example questions")
    print("Type 'stream' to enable streaming mode")
    print("=" * 60)
    
    chatbot = JavaChatbot(api_key)
    streaming_chatbot = GroqJavaChatbot(api_key)
    use_streaming = False
    
    while True:
        user_input = input("\n💭 Your Question: ").strip()
        
        if user_input.lower() == 'exit':
            print("👋 Goodbye! Keep coding securely!")
            break
        
        if user_input.lower() == 'stream':
            use_streaming = not use_streaming
            mode = "enabled" if use_streaming else "disabled"
            print(f"🔄 Streaming mode {mode}")
            continue
        
        if user_input.lower() == 'samples':
            samples = chatbot.get_sample_questions()
            print("\n📚 Sample Questions (Security & MVC Focused):")
            for category, questions in samples.items():
                print(f"\n{category}:")
                for i, question in enumerate(questions, 1):
                    print(f"  {i}. {question}")
            continue
        
        if not user_input:
            print("❌ Please enter a valid question.")
            continue
        
        print("\n🤖 Secure & MVC-Compliant Response:")
        print("-" * 40)
        
        if use_streaming:
            response = streaming_chatbot.stream_response(user_input)
        else:
            response = chatbot.get_response(user_input)
            print(response)
        
        print("-" * 40)

if __name__ == "__main__":
    main()