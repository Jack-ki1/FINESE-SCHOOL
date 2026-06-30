"""
Test script to verify Flask transformation setup
Run with: py test_flask_setup.py
"""

import os
import sys

def check_dependencies():
    """Check if all required packages are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'flask',
        'pydantic',
        'python-dotenv',
        'reportlab',
        'markdown',
        'bleach'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Install with: pip install " + " ".join(missing))
        return False
    
    print("\n✅ All dependencies installed!\n")
    return True


def check_file_structure():
    """Check if all required files exist"""
    print("📁 Checking file structure...")
    
    required_files = [
        'app.py',
        'templates/index.html',
        'static/css/style.css',
        'config.py',
        'src/chat_engine.py',
        'src/models.py',
        'src/pdf_export.py',
        'src/config.py'
    ]
    
    missing = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - NOT FOUND")
            missing.append(file_path)
    
    if missing:
        print(f"\n⚠️  Missing files: {len(missing)}")
        for f in missing:
            print(f"   - {f}")
        return False
    
    print("\n✅ All required files present!\n")
    return True


def check_env_file():
    """Check if .env file exists"""
    print("🔐 Checking environment configuration...")
    
    if os.path.exists('.env'):
        print("✅ .env file found")
        
        # Check for API key
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('HUGGINGFACE_API_KEY')
        if api_key and api_key != 'your_huggingface_token_here':
            print("✅ Hugging Face API key configured")
            return True
        else:
            print("⚠️  Please add your Hugging Face API key to .env file")
            print("   Get one at: https://huggingface.co/settings/tokens")
            return False
    else:
        print("❌ .env file not found")
        print("   Create one: cp .env.example .env")
        return False


def test_imports():
    """Test if main modules can be imported"""
    print("\n🧪 Testing module imports...")
    
    try:
        from src.config import TOPIC_REGISTRY
        print(f"✅ Config loaded - {len(TOPIC_REGISTRY)} topics available")
        
        from src.models import TutorResponse
        print("✅ Models imported successfully")
        
        from src.chat_engine import generate_structured_response
        print("✅ Chat engine imported successfully")
        
        from src.pdf_export import export_chat_to_pdf
        print("✅ PDF export imported successfully")
        
        print("\n✅ All modules imported successfully!\n")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False


def main():
    """Run all checks"""
    print("=" * 60)
    print("🎓 FINESE SCHOOL - Flask Transformation Setup Test")
    print("=" * 60)
    print()
    
    checks = [
        ("Dependencies", check_dependencies),
        ("File Structure", check_file_structure),
        ("Environment", check_env_file),
        ("Module Imports", test_imports)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} check failed: {e}")
            results.append((name, False))
        print()
    
    # Summary
    print("=" * 60)
    print("📊 Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print()
    print(f"Result: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 All checks passed! Ready to run the app.")
        print("\nStart the application with:")
        print("   py app.py")
        print("\nThen visit: http://localhost:5000")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
    
    print("=" * 60)
    
    return passed == total


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
