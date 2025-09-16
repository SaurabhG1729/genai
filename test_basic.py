"""
Simple test script to verify the legal document demystifier works
Run this after installing the required packages
"""

def test_basic_functionality():
    """Test basic functionality without AI dependencies"""
    print("🧪 Testing Legal Document Demystifier...")
    
    try:
        # Test 1: Import the main class
        from main import LegalDocumentDemystifier, create_sample_legal_text
        print("✅ Successfully imported main classes")
        
        # Test 2: Create sample text
        sample_text = create_sample_legal_text()
        print(f"✅ Sample text created ({len(sample_text)} characters)")
        
        # Test 3: Initialize demystifier
        try:
            demystifier = LegalDocumentDemystifier(ai_provider="huggingface")
            print("✅ Demystifier initialized with Hugging Face")
        except:
            try:
                demystifier = LegalDocumentDemystifier(ai_provider="openai")
                print("✅ Demystifier initialized with OpenAI")
            except:
                print("⚠️  No AI provider available, but class works")
        
        # Test 4: Text processing functions
        cleaned_text = demystifier.clean_text(sample_text)
        print(f"✅ Text cleaning works ({len(cleaned_text)} characters)")
        
        # Test 5: Key term extraction
        key_terms = demystifier.extract_key_terms(sample_text)
        print(f"✅ Key term extraction works ({len(key_terms)} terms found)")
        
        print("\n🎉 All basic tests passed!")
        print("\n📋 To run the full program, execute: python main.py")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("\n💡 Make sure to install required packages:")
        print("   pip install transformers torch PyPDF2")
        print("   or")
        print("   pip install openai PyPDF2")

if __name__ == "__main__":
    test_basic_functionality()