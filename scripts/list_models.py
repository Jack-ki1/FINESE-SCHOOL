#!/usr/bin/env python3
"""List available models for the configured GOOGLE_API_KEY.

Run:
  $env:GOOGLE_API_KEY="your_key_here"
  python .\scripts\list_models.py

This prints a sample of models you can set as MODEL_NAME.
"""
import os
import sys
import json

try:
    from langchain_google_genai import GoogleGenerativeAI
except Exception as e:
    print("Missing dependency: langchain_google_genai (or import failed):", e)
    sys.exit(2)


def main():
    key = os.getenv("GOOGLE_API_KEY")
    if not key:
        print("ERROR: Set the GOOGLE_API_KEY environment variable before running this script.")
        print("In PowerShell: $env:GOOGLE_API_KEY=\"your_key_here\"")
        print("In Bash/Mac/Linux: export GOOGLE_API_KEY=\"your_key_here\"")
        return

    print("🔍 Connecting to Google Generative AI...")
    client = GoogleGenerativeAI(google_api_key=key)
    
    try:
        print("🔄 Fetching available models...")
        models = client.list_models()
    except Exception as e:
        print("❌ Failed to list models:", e)
        print("\n💡 Troubleshooting tips:")
        print("   1. Check that your API key is valid and properly set")
        print("   2. Ensure you have internet connectivity")
        print("   3. Check if there are any firewall restrictions")
        return

    print("\n✅ Available models:")
    print("=" * 60)
    
    # models may be a list of strings or dict-like objects; print readable representation
    try:
        model_list = []
        for i, m in enumerate(models):
            if hasattr(m, 'name'):
                # It's likely a Model object
                model_name = m.name.replace('models/', '') if m.name.startswith('models/') else m.name
                model_list.append(model_name)
                print(f"{i+1:2d}. {model_name}")
            else:
                # It's likely a string or dict
                model_str = str(m)
                model_name = model_str.replace('models/', '') if model_str.startswith('models/') else model_str
                model_list.append(model_name)
                print(f"{i+1:2d}. {model_name}")
                
        print(f"\n📊 Total models found: {len(model_list)}")
    except TypeError:
        print(models)
    
    print("\n📝 To use a specific model, set the MODEL_NAME environment variable:")
    print("PowerShell: $env:MODEL_NAME=\"model_name_from_list\"")
    print("Bash/Linux: export MODEL_NAME=\"model_name_from_list\"")
    
    print("\n⭐ Recommended models:")
    recommended = [m for m in model_list if any(r in m.lower() for r in ['gemini-1.5', 'gemini-pro', 'gemma'])]
    for model in recommended[:5]:
        print(f"  • {model}")

if __name__ == "__main__":
    main()