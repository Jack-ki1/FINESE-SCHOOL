"""
Test Google Gemini API connection with correct model names
Run with: py test_google_gemini.py
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("🧪 Testing Google Gemini API Connection")
print("=" * 60)
print()

# Check environment variables
print("1. Checking environment variables...")
api_type = os.getenv('API_TYPE')
google_key = os.getenv('GOOGLE_API_KEY')
gemini_model = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')

print(f"   API_TYPE: {api_type}")
print(f"   GOOGLE_API_KEY: {'✅ Set' if google_key else '❌ NOT SET'}")
if google_key:
    print(f"      (starts with: {google_key[:10]}...)")
print(f"   GEMINI_MODEL: {gemini_model}")
print()

if api_type != 'google':
    print("⚠️  WARNING: API_TYPE is not set to 'google'")
    print(f"   Current value: '{api_type}'")
    print("   Please update .env file: API_TYPE=google")
    print()

if not google_key:
    print("❌ ERROR: GOOGLE_API_KEY is not set!")
    print("   Please add your API key to .env file")
    exit(1)

# Try to import and initialize
print("2. Testing Google Gemini initialization...")
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    print("   ✅ langchain-google-genai imported successfully")
except ImportError as e:
    print(f"   ❌ Failed to import: {e}")
    print("   Install with: pip install langchain-google-genai")
    exit(1)

# Test different model names
models_to_try = [
    "gemini-1.5-flash-latest",
    "gemini-1.5-pro-latest", 
    "gemini-pro",
    "gemini-1.0-pro",
    gemini_model  # Try the configured one last
]

llm = None
working_model = None

for model_name in models_to_try:
    try:
        print(f"\n3. Testing model: {model_name}...")
        llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=0.3,
            max_output_tokens=2048,
            google_api_key=google_key,
            convert_system_message_to_human=True
        )
        
        print(f"   Sending test message...")
        response = llm.invoke("Say 'Google Gemini is working!' in one sentence.")
        print(f"   ✅ SUCCESS! Model '{model_name}' works!")
        print(f"   Response: {response.content}")
        working_model = model_name
        break
        
    except Exception as e:
        error_msg = str(e)
        if "NOT_FOUND" in error_msg or "not found" in error_msg.lower():
            print(f"   ❌ Model '{model_name}' not found")
        elif "404" in error_msg:
            print(f"   ❌ Model '{model_name}' returned 404")
        else:
            print(f"   ❌ Error with '{model_name}': {error_msg[:100]}")

if not working_model:
    print("\n" + "=" * 60)
    print("❌ No working model found!")
    print("=" * 60)
    print("\nPossible issues:")
    print("1. API key might be invalid or expired")
    print("2. Google Cloud project not configured for Gemini API")
    print("3. API quota exceeded")
    print("4. Billing not enabled on Google Cloud")
    print("\nTo fix:")
    print("1. Visit: https://makersuite.google.com/")
    print("2. Create a new API key")
    print("3. Update .env file with new key")
    print("4. Ensure billing is enabled on Google Cloud Console")
    exit(1)

# Update .env file with working model
print("\n" + "=" * 60)
print(f"✅ Found working model: {working_model}")
print("=" * 60)
print(f"\nPlease update your .env file:")
print(f"GEMINI_MODEL={working_model}")
print(f"\nThen restart Flask app: py app.py")
