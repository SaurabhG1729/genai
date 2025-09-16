"""
Legal Document Demystifier
A student project to simplify legal documents using Generative AI

This prototype demonstrates how to use AI to make legal documents more understandable.
"""

import os
import re
import json
from typing import Dict, List, Optional
from datetime import datetime

# Try to import required libraries with fallback options
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("OpenAI library not installed. Install with: pip install openai")

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("Transformers library not installed. Install with: pip install transformers torch")

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("PyPDF2 not installed. Install with: pip install PyPDF2")


class LegalDocumentDemystifier:
    """
    A class to simplify legal documents using AI
    """
    
    def __init__(self, ai_provider="openai"):
        """
        Initialize the demystifier with chosen AI provider
        
        Args:
            ai_provider (str): "openai" or "huggingface"
        """
        self.ai_provider = ai_provider
        self.setup_ai()
        
    def setup_ai(self):
        """Set up the chosen AI provider"""
        if self.ai_provider == "openai" and OPENAI_AVAILABLE:
            # Set up OpenAI (user needs to set their API key)
            openai.api_key = os.getenv("OPENAI_API_KEY")
            if not openai.api_key:
                print("⚠️  OpenAI API key not found. Set OPENAI_API_KEY environment variable")
                print("   Or get a key from: https://platform.openai.com/api-keys")
        
        elif self.ai_provider == "huggingface" and TRANSFORMERS_AVAILABLE:
            # Set up Hugging Face pipeline (free, no API key needed)
            print("🔄 Loading Hugging Face model (this may take a moment)...")
            try:
                # Use a smaller, faster model for demo purposes
                self.summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
                print("✅ Hugging Face model loaded successfully!")
            except Exception as e:
                print(f"❌ Error loading Hugging Face model: {e}")
                print("💡 Falling back to simple text processing...")
                self.summarizer = None
        else:
            print("❌ No AI provider available. Please install required libraries.")
    
    def read_text_file(self, file_path: str) -> str:
        """Read text from a .txt file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"❌ Error reading text file: {e}")
            return ""
    
    def read_pdf_file(self, file_path: str) -> str:
        """Read text from a PDF file"""
        if not PDF_AVAILABLE:
            print("❌ PyPDF2 not available. Cannot read PDF files.")
            return ""
        
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"❌ Error reading PDF file: {e}")
            return ""
    
    def clean_text(self, text: str) -> str:
        """Clean and preprocess the legal text"""
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters that might confuse the AI
        text = re.sub(r'[^\w\s.,;:!?()-]', '', text)
        return text.strip()
    
    def extract_key_terms(self, text: str) -> List[str]:
        """Extract potential legal terms from the text"""
        # Common legal term patterns
        legal_patterns = [
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+Agreement\b',  # "Service Agreement"
            r'\bterms?\s+(?:and\s+)?conditions?\b',  # "terms and conditions"
            r'\bliability\b', r'\bindemnif\w+\b', r'\bwarrant\w+\b',
            r'\bgoverning\s+law\b', r'\bjurisdiction\b', r'\barbitration\b'
        ]
        
        terms = []
        for pattern in legal_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            terms.extend(matches)
        
        return list(set(terms))  # Remove duplicates
    
    def simplify_with_openai(self, text: str) -> Dict[str, str]:
        """Use OpenAI to simplify legal text"""
        if not OPENAI_AVAILABLE or not openai.api_key:
            return {"error": "OpenAI not available or API key not set"}
        
        try:
            # Create prompts for different types of simplification
            prompts = {
                "summary": f"""
                Please provide a simple, easy-to-understand summary of this legal document.
                Use everyday language and explain what this document means for a regular person:
                
                {text[:2000]}  # Limit text length for API
                """,
                
                "key_points": f"""
                Extract the 5 most important points from this legal document.
                Explain each point in simple terms that a student could understand:
                
                {text[:2000]}
                """,
                
                "risks": f"""
                What are the potential risks or important things someone should know 
                before agreeing to this legal document? Explain in simple terms:
                
                {text[:2000]}
                """
            }
            
            results = {}
            for prompt_type, prompt in prompts.items():
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",  # Using cheaper model for student project
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500,
                    temperature=0.3
                )
                results[prompt_type] = response.choices[0].message.content
            
            return results
            
        except Exception as e:
            return {"error": f"OpenAI API error: {e}"}
    
    def simplify_with_basic_processing(self, text: str) -> Dict[str, str]:
        """Basic text processing when AI models are not available"""
        sentences = text.split('. ')
        
        # Create a simple summary by taking first few sentences
        summary_sentences = sentences[:3]
        summary = '. '.join(summary_sentences) + '.'
        
        # Extract key points (sentences with important words)
        important_words = ['agree', 'shall', 'liable', 'payment', 'terminate', 'confidential']
        key_sentences = []
        
        for sentence in sentences:
            if any(word in sentence.lower() for word in important_words):
                key_sentences.append(sentence.strip())
        
        key_points = '\n'.join([f"• {sentence}" for sentence in key_sentences[:5]])
        
        # Basic risk identification
        risk_words = ['liable', 'penalty', 'terminate', 'breach', 'default']
        risk_sentences = []
        
        for sentence in sentences:
            if any(word in sentence.lower() for word in risk_words):
                risk_sentences.append(sentence.strip())
        
        risks = '\n'.join([f"⚠️ {sentence}" for sentence in risk_sentences[:3]])
        
        return {
            "summary": f"📄 Basic Summary (No AI model available):\n{summary}",
            "key_points": f"🎯 Key Points Found:\n{key_points}" if key_points else "No key points identified with basic processing.",
            "risks": f"⚠️ Potential Concerns:\n{risks}" if risks else "No obvious risks identified with basic processing."
        }
    
    def simplify_with_huggingface(self, text: str) -> Dict[str, str]:
        """Use Hugging Face to simplify legal text"""
        if not TRANSFORMERS_AVAILABLE:
            return {"error": "Hugging Face model not available"}
        
        # If model is not loaded, fall back to simple text processing
        if not self.summarizer:
            return self.simplify_with_basic_processing(text)
        
        try:
            # Split text into chunks if it's too long
            max_chunk_length = 1024
            chunks = [text[i:i+max_chunk_length] for i in range(0, len(text), max_chunk_length)]
            
            summaries = []
            for chunk in chunks[:3]:  # Limit to first 3 chunks for demo
                if len(chunk.strip()) > 100:  # Only summarize substantial chunks
                    summary = self.summarizer(chunk, max_length=150, min_length=50, do_sample=False)
                    summaries.append(summary[0]['summary_text'])
            
            return {
                "summary": " ".join(summaries),
                "key_points": "Key points extraction requires OpenAI API for this demo",
                "risks": "Risk analysis requires OpenAI API for this demo"
            }
            
        except Exception as e:
            print(f"❌ Hugging Face model error: {e}")
            print("💡 Falling back to basic text processing...")
            return self.simplify_with_basic_processing(text)
    
    def analyze_document(self, file_path: str) -> Dict:
        """
        Main method to analyze a legal document
        
        Args:
            file_path (str): Path to the legal document
            
        Returns:
            Dict: Analysis results
        """
        print(f"🔍 Analyzing document: {file_path}")
        
        # Read the document
        if file_path.lower().endswith('.pdf'):
            text = self.read_pdf_file(file_path)
        else:
            text = self.read_text_file(file_path)
        
        if not text:
            return {"error": "Could not read the document"}
        
        # Clean the text
        cleaned_text = self.clean_text(text)
        
        # Extract basic information
        word_count = len(cleaned_text.split())
        char_count = len(cleaned_text)
        
        print(f"📄 Document loaded: {word_count} words, {char_count} characters")
        
        # Extract key terms
        key_terms = self.extract_key_terms(cleaned_text)
        
        # Get AI analysis
        print(f"🤖 Getting AI analysis using {self.ai_provider}...")
        if self.ai_provider == "openai":
            ai_results = self.simplify_with_openai(cleaned_text)
        else:
            ai_results = self.simplify_with_huggingface(cleaned_text)
        
        # Compile results
        results = {
            "document_info": {
                "file_path": file_path,
                "word_count": word_count,
                "character_count": char_count,
                "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "key_terms": key_terms,
            "ai_analysis": ai_results,
            "original_text_preview": cleaned_text[:500] + "..." if len(cleaned_text) > 500 else cleaned_text
        }
        
        return results
    
    def print_results(self, results: Dict):
        """Print analysis results in a formatted way"""
        print("\n" + "="*60)
        print("📋 LEGAL DOCUMENT ANALYSIS RESULTS")
        print("="*60)
        
        # Document info
        info = results.get("document_info", {})
        print(f"\n📄 Document: {info.get('file_path', 'Unknown')}")
        print(f"📊 Stats: {info.get('word_count', 0)} words, {info.get('character_count', 0)} characters")
        print(f"🕒 Analyzed: {info.get('analysis_date', 'Unknown')}")
        
        # Key terms
        key_terms = results.get("key_terms", [])
        if key_terms:
            print(f"\n🎯 KEY LEGAL TERMS FOUND:")
            for term in key_terms[:10]:  # Show first 10 terms
                print(f"  • {term}")
        
        # AI Analysis
        ai_analysis = results.get("ai_analysis", {})
        if "error" in ai_analysis:
            print(f"\n❌ AI Analysis Error: {ai_analysis['error']}")
        else:
            print(f"\n🤖 AI ANALYSIS RESULTS:")
            
            if "summary" in ai_analysis:
                print(f"\n📝 SUMMARY:")
                print(f"{ai_analysis['summary']}")
            
            if "key_points" in ai_analysis:
                print(f"\n🎯 KEY POINTS:")
                print(f"{ai_analysis['key_points']}")
            
            if "risks" in ai_analysis:
                print(f"\n⚠️  POTENTIAL RISKS/IMPORTANT NOTES:")
                print(f"{ai_analysis['risks']}")
        
        print("\n" + "="*60)
    
    def save_results(self, results: Dict, output_path: str):
        """Save results to a JSON file"""
        try:
            with open(output_path, 'w', encoding='utf-8') as file:
                json.dump(results, file, indent=2, ensure_ascii=False)
            print(f"💾 Results saved to: {output_path}")
        except Exception as e:
            print(f"❌ Error saving results: {e}")


def create_sample_legal_text():
    """Create a sample legal document for testing"""
    sample_text = """
    SERVICE AGREEMENT
    
    This Service Agreement ("Agreement") is entered into on [DATE] between Company XYZ ("Provider") 
    and the Client ("Client").
    
    1. SERVICES
    Provider agrees to perform consulting services as described in Exhibit A. All services shall be 
    performed in a professional and workmanlike manner in accordance with industry standards.
    
    2. PAYMENT TERMS
    Client agrees to pay Provider the fees set forth in Exhibit A. Payment is due within thirty (30) 
    days of invoice date. Late payments may incur a fee of 1.5% per month.
    
    3. CONFIDENTIALITY
    Both parties acknowledge that they may have access to confidential information. Each party agrees 
    to maintain the confidentiality of such information and not disclose it to third parties.
    
    4. LIMITATION OF LIABILITY
    Provider's liability shall not exceed the total amount paid by Client under this Agreement. 
    Provider shall not be liable for any indirect, incidental, or consequential damages.
    
    5. GOVERNING LAW
    This Agreement shall be governed by the laws of [STATE]. Any disputes shall be resolved through 
    binding arbitration.
    
    6. TERMINATION
    Either party may terminate this Agreement with thirty (30) days written notice.
    """
    
    return sample_text


def main():
    """Main function to run the legal document demystifier"""
    print("🏛️  Legal Document Demystifier - Student Project")
    print("="*50)
    
    # Check available AI providers
    print("\n🔍 Checking available AI providers...")
    if OPENAI_AVAILABLE:
        print("✅ OpenAI library available")
    if TRANSFORMERS_AVAILABLE:
        print("✅ Transformers library available")
    if not OPENAI_AVAILABLE and not TRANSFORMERS_AVAILABLE:
        print("❌ No AI libraries available. Please install openai or transformers.")
        return
    
    # Choose AI provider
    if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
        ai_provider = "openai"
        print("🤖 Using OpenAI API")
    elif TRANSFORMERS_AVAILABLE:
        ai_provider = "huggingface"
        print("🤖 Using Hugging Face (free, local)")
    else:
        print("❌ No usable AI provider found.")
        print("💡 Set OPENAI_API_KEY environment variable or install transformers")
        return
    
    # Initialize the demystifier
    demystifier = LegalDocumentDemystifier(ai_provider=ai_provider)
    
    # Demo options
    print("\n📋 Choose an option:")
    print("1. Analyze a sample legal document (built-in)")
    print("2. Analyze your own document file")
    print("3. Test with custom text")
    
    try:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            # Use sample document
            print("\n📄 Using built-in sample legal document...")
            sample_text = create_sample_legal_text()
            
            # Save sample to file for analysis
            sample_file = "sample_legal_document.txt"
            with open(sample_file, 'w', encoding='utf-8') as f:
                f.write(sample_text)
            
            results = demystifier.analyze_document(sample_file)
            demystifier.print_results(results)
            
            # Clean up
            os.remove(sample_file)
            
        elif choice == "2":
            # User's own file
            file_path = input("Enter the path to your legal document: ").strip()
            if os.path.exists(file_path):
                results = demystifier.analyze_document(file_path)
                demystifier.print_results(results)
                
                # Option to save results
                save_choice = input("\nSave results to file? (y/n): ").strip().lower()
                if save_choice == 'y':
                    output_file = f"analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    demystifier.save_results(results, output_file)
            else:
                print(f"❌ File not found: {file_path}")
        
        elif choice == "3":
            # Custom text input
            print("\n📝 Enter your legal text (press Enter twice when done):")
            lines = []
            while True:
                line = input()
                if line == "" and len(lines) > 0:
                    break
                lines.append(line)
            
            custom_text = "\n".join(lines)
            if custom_text.strip():
                # Save custom text to temporary file
                temp_file = "temp_legal_text.txt"
                with open(temp_file, 'w', encoding='utf-8') as f:
                    f.write(custom_text)
                
                results = demystifier.analyze_document(temp_file)
                demystifier.print_results(results)
                
                # Clean up
                os.remove(temp_file)
            else:
                print("❌ No text entered.")
        
        else:
            print("❌ Invalid choice.")
    
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")


if __name__ == "__main__":
    main()
