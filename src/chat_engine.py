import os
import logging
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from src.config import TOPIC_REGISTRY, MODEL_NAME, TEMPERATURE, MAX_TOKENS
from src.models import TutorResponse

# Conditional imports based on available API
try:
    from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAI
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False
    logging.warning("Google Generative AI library not available")

try:
    from langchain_huggingface import HuggingFaceEndpoint
    HUGGINGFACE_API_AVAILABLE = True
except ImportError:
    HUGGINGFACE_API_AVAILABLE = False
    logging.warning("HuggingFace library not available")

try:
    from langchain_openai import ChatOpenAI
    OPENAI_API_AVAILABLE = True
except ImportError:
    OPENAI_API_AVAILABLE = False
    logging.warning("OpenAI library not available")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_llm():
    # Determine which API to use based on environment variables
    api_type = os.getenv("API_TYPE", "huggingface").lower()
    
    if api_type == "google" and GOOGLE_API_AVAILABLE:
        return get_google_llm()
    elif api_type == "openai" and OPENAI_API_AVAILABLE:
        return get_openai_llm()
    elif api_type == "huggingface" and HUGGINGFACE_API_AVAILABLE:
        return get_huggingface_llm()
    else:
        # Fallback to HuggingFace if preferred option is not available
        if HUGGINGFACE_API_AVAILABLE:
            return get_huggingface_llm()
        elif GOOGLE_API_AVAILABLE:
            return get_google_llm()
        elif OPENAI_API_AVAILABLE:
            return get_openai_llm()
        else:
            raise RuntimeError("No suitable LLM API available. Please install one of: langchain-google-genai, langchain-huggingface, langchain-openai")

def get_google_llm():
    key = os.getenv("GOOGLE_API_KEY")
    if not key:
        raise RuntimeError("GOOGLE_API_KEY is required for Google API")
    
    # Use Gemini model - use GEMINI_MODEL environment variable specifically for Google, fallback to gemini-1.5-flash
    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
    logger.info(f"Initializing Google Gemini LLM with model: {model_name}")
    logger.info(f"API Key starts with: {key[:10]}...")  # Log first 10 chars for verification
    
    try:
        llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=TEMPERATURE,
            max_output_tokens=MAX_TOKENS,  # Changed from max_tokens to max_output_tokens for Gemini
            google_api_key=key,
            convert_system_message_to_human=True  # Required for Gemini in LangChain
        )
        
        # Test the connection with a simple call
        logger.info("Testing Google Gemini connection...")
        test_response = llm.invoke("Say 'Connection successful'")
        logger.info(f"Test response: {test_response.content}")
        
        return llm
        
    except Exception as e:
        logger.error(f"Failed to initialize Google Gemini: {str(e)}")
        raise RuntimeError(f"Google Gemini initialization failed: {str(e)}. Check your API key and model name.")

def get_openai_llm():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required for OpenAI API")
    
    # Ensure model name is set
    model_name = MODEL_NAME if MODEL_NAME else "gpt-3.5-turbo"
    
    logger.info(f"Initializing OpenAI LLM with model: {model_name}")
    
    return ChatOpenAI(
        model_name=model_name,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        openai_api_key=key
    )

# ... existing code ...
def get_huggingface_llm():
    key = os.getenv("HUGGINGFACE_API_KEY")
    
    # Check if API key is provided
    if not key:
        raise RuntimeError("HUGGINGFACE_API_KEY is required for Hugging Face API. Please set your API key.")
    
    # Default to a good open-source model if none specified
    model_name = MODEL_NAME if MODEL_NAME else "mistralai/Mistral-7B-Instruct-v0.2"
    
    logger.info(f"Initializing HuggingFace LLM with model: {model_name}")
    
    # Determine appropriate task based on model
    task = "text-generation"
    if "zephyr" in model_name.lower() or "dialo" in model_name.lower() or "mistral" in model_name.lower():
        task = "conversational"
    elif "flan" in model_name.lower():
        task = "text2text-generation"
    elif "t5" in model_name.lower():
        task = "text2text-generation"
        
    # Try to initialize the HuggingFace endpoint
    try:
        return HuggingFaceEndpoint(
            repo_id=model_name,
            huggingfacehub_api_token=key,
            task=task,
            temperature=TEMPERATURE,
            max_new_tokens=MAX_TOKENS,
            
        )
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Hugging Face model {model_name}: {str(e)}")

def validate_model_availability(model_name: str, api_key: str):
    """
    Validate if the specified model is available for the given API key.
    
    Args:
        model_name: Name of the model to check
        api_key: API key
    
    Raises:
        RuntimeError: If the model is not available
    """
    # Simplified validation approach
    logger.warning("Model validation is not implemented for all providers. Proceeding with initialization.")
    pass

def build_expert_prompt(topic_spec, user_question: str) -> ChatPromptTemplate:
    parser = PydanticOutputParser(pydantic_object=TutorResponse)
    
    system_message = f"""
You are Dr. Data, a world-class data science educator with PhDs in CS and Statistics.
You are tutoring a professional on: **{topic_spec.name}**
Context:
- Allowed libraries: {', '.join(topic_spec.allowed_libraries) or 'None'}
- Avoid: {', '.join(topic_spec.banned_topics) or 'Nothing'}
- Style: {topic_spec.style_guide}
Rules:
1. If the question is off-topic (e.g., about web dev in a Pandas session), set is_on_topic=False and give a polite redirect.
2. Always attempt diagnosis: what might the user be confused about?
3. Code must be minimal, correct, and include necessary imports.
4. Cite official documentation when possible.
5. NEVER hallucinate package functions.
6. Output ONLY in the requested JSON format.
{{format_instructions}}
"""
    
    return ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_message),
        ("human", "Question: {question}")
    ])

def generate_structured_response(topic_key: str, user_question: str) -> TutorResponse:
    try:
        llm = get_llm()
    except Exception as e:
        raise RuntimeError(f"Failed to initialize LLM: {str(e)}")
    
    topic_spec = TOPIC_REGISTRY[topic_key]
    
    # Create parser
    parser = PydanticOutputParser(pydantic_object=TutorResponse)
    
    # Build prompt with proper variable names
    prompt = build_expert_prompt(topic_spec, user_question)
    
    # Create the chain with proper variable binding
    chain = prompt.partial(format_instructions=parser.get_format_instructions()) | llm
    
    # Invoke with the question
    try:
        raw_output = chain.invoke({"question": user_question})
        logger.info(f"Raw LLM output: {raw_output.content[:200]}...")
    except Exception as e:
        error_msg = str(e).lower()
        if "401" in error_msg or "unauthorized" in error_msg:
            detailed_msg = "API key is invalid or expired. Please check your API key in the sidebar settings."
        elif "429" in error_msg or "rate limit" in error_msg:
            detailed_msg = "Rate limit exceeded. Please wait a few minutes or check your API plan limits."
        elif "connection" in error_msg or "timeout" in error_msg:
            detailed_msg = "Network connection issue. Please check your internet connection and try again."
        elif "model" in error_msg and "not found" in error_msg:
            detailed_msg = f"Model '{MODEL_NAME}' not available. Please select a valid model from the dropdown or check spelling."
        else:
            detailed_msg = f"Unexpected error: {str(e)}. Please check your model configuration."
        raise RuntimeError(f"Failed to get response from LLM: {detailed_msg}")
    
    # Parse and validate
    try:
        response = parser.parse(raw_output.content)
    except Exception as e:
        # Try to extract JSON from the response if parsing fails
        import re
        import json
        
        # Look for JSON in the response
        json_match = re.search(r'\{.*\}', raw_output.content, re.DOTALL)
        if json_match:
            try:
                json_str = json_match.group(0)
                # Fix common JSON issues
                json_str = json_str.replace('\n', '').replace('\t', '')
                # Parse and reconstruct response
                json_data = json.loads(json_str)
                response = TutorResponse(**json_data)
            except Exception as json_e:
                raise ValueError(f"Failed to parse LLM output as JSON: {json_e}\nOriginal error: {e}\nRaw: {raw_output.content[:500]}...")
        else:
            # Fallback: retry with stricter prompt or return error
            raise ValueError(f"Failed to parse LLM output: {e}\nRaw: {raw_output.content[:500]}...")
    
    return response