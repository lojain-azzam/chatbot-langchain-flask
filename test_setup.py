#!/usr/bin/env python3
"""
Test script to verify the LangChain Flask chatbot setup.
This script checks dependencies, imports, and basic functionality.
"""

import sys
import os
from importlib import import_module

def test_imports():
    """Test if all required modules can be imported."""
    print("Testing imports...")
    
    required_modules = [
        'flask',
        'langchain',
        'langchain_openai',
        'openai',
        'dotenv'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            import_module(module)
            print(f"✓ {module}")
        except ImportError as e:
            print(f"✗ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\nFailed to import: {', '.join(failed_imports)}")
        print("Please run: pip install -r requirements.txt")
        return False
    
    print("All imports successful!\n")
    return True

def test_app_import():
    """Test if the main app can be imported."""
    print("Testing app import...")
    
    try:
        # Add current directory to path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Try to import the app
        from app import app, chatbot_manager
        print("✓ App imported successfully")
        
        # Test chatbot manager initialization
        print("✓ ChatbotManager initialized")
        
        return True
        
    except Exception as e:
        print(f"✗ Failed to import app: {e}")
        return False

def test_environment():
    """Test environment setup."""
    print("Testing environment...")
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✓ .env file found")
    else:
        print("⚠ .env file not found (create one from env_example.txt)")
    
    # Check for API keys
    from dotenv import load_dotenv
    load_dotenv()
    
    openai_key = os.getenv('OPENAI_API_KEY')
    google_key = os.getenv('GOOGLE_API_KEY')
    
    if openai_key and openai_key != 'your_openai_api_key_here':
        print("✓ OpenAI API key configured")
    else:
        print("⚠ OpenAI API key not configured")
    
    if google_key and google_key != 'your_google_api_key_here':
        print("✓ Google API key configured")
    else:
        print("⚠ Google API key not configured")
    
    if not openai_key and not google_key:
        print("⚠ No API keys configured - chatbot will not work")
        return False
    
    return True

def test_file_structure():
    """Test if all required files exist."""
    print("Testing file structure...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'templates/index.html',
        'static/css/style.css',
        'static/js/chat.js',
        'README.md'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\nMissing files: {', '.join(missing_files)}")
        return False
    
    print("All files present!\n")
    return True

def main():
    """Run all tests."""
    print("=" * 50)
    print("LangChain Flask Chatbot - Setup Test")
    print("=" * 50)
    print()
    
    tests = [
        ("File Structure", test_file_structure),
        ("Imports", test_imports),
        ("App Import", test_app_import),
        ("Environment", test_environment)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"Running {test_name} test...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} test failed with error: {e}")
            results.append((test_name, False))
        print()
    
    # Summary
    print("=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! Your setup is ready.")
        print("\nTo run the chatbot:")
        print("1. Configure your API keys in .env file")
        print("2. Run: python app.py")
        print("3. Open: http://localhost:5000")
    else:
        print("\n❌ Some tests failed. Please fix the issues above.")
        print("\nCommon solutions:")
        print("- Run: pip install -r requirements.txt")
        print("- Create .env file from env_example.txt")
        print("- Add your API keys to .env file")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 