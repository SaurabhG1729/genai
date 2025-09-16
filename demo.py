"""
Legal Document Demystifier - Lightweight Demo Version
Works immediately without downloading any models
"""

import os
import re
import json
from typing import Dict, List
from datetime import datetime


class SimpleLegalDemystifier:
    """
    A lightweight legal document analyzer that works without AI models
    Perfect for testing and learning
    """
    
    def __init__(self):
        print("✅ Simple Legal Demystifier initialized (no downloads required)")
    
    def read_text_file(self, file_path: str) -> str:
        """Read text from a .txt file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"❌ Error reading text file: {e}")
            return ""
    
    def clean_text(self, text: str) -> str:
        """Clean and preprocess the legal text"""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s.,;:!?()-]', '', text)
        return text.strip()
    
    def extract_key_terms(self, text: str) -> List[str]:
        """Extract legal terms from the text"""
        legal_patterns = [
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+Agreement\b',
            r'\bterms?\s+(?:and\s+)?conditions?\b',
            r'\bliability\b', r'\bindemnif\w+\b', r'\bwarrant\w+\b',
            r'\bgoverning\s+law\b', r'\bjurisdiction\b', r'\barbitration\b',
            r'\bconfidential\w*\b', r'\btermination\b', r'\bpayment\b'
        ]
        
        terms = []
        for pattern in legal_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            terms.extend(matches)
        
        return list(set(terms))
    
    def analyze_document_structure(self, text: str) -> Dict[str, any]:
        """Analyze the structure of the legal document"""
        lines = text.split('\n')
        
        # Find numbered sections
        sections = []
        for line in lines:
            if re.match(r'^\s*\d+\.', line.strip()):
                sections.append(line.strip())
        
        # Count sentences and paragraphs
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        return {
            "sections": sections,
            "sentence_count": len(sentences),
            "paragraph_count": len(paragraphs),
            "avg_sentence_length": sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
        }
    
    def create_simple_summary(self, text: str) -> str:
        """Create a basic summary using rule-based approach"""
        sentences = [s.strip() for s in text.split('.') if s.strip() and len(s) > 20]
        
        # Take first sentence and sentences with key legal terms
        summary_sentences = []
        
        # Always include first sentence (usually the main declaration)
        if sentences:
            summary_sentences.append(sentences[0])
        
        # Add sentences with important legal concepts
        important_indicators = [
            'agree', 'shall', 'payment', 'liability', 'termination',
            'confidential', 'governing law', 'dispute'
        ]
        
        for sentence in sentences[1:]:
            if any(indicator in sentence.lower() for indicator in important_indicators):
                if len(summary_sentences) < 4:  # Limit summary length
                    summary_sentences.append(sentence)
        
        return '. '.join(summary_sentences) + '.'
    
    def extract_key_obligations(self, text: str) -> List[str]:
        """Extract key obligations and requirements"""
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        obligations = []
        
        # Look for sentences with obligation indicators
        obligation_words = ['shall', 'must', 'agrees to', 'required to', 'responsible for']
        
        for sentence in sentences:
            if any(word in sentence.lower() for word in obligation_words):
                # Simplify the sentence
                simplified = sentence.replace('The Client', 'You')
                simplified = simplified.replace('The Provider', 'The service provider')
                simplified = simplified.replace('shall', 'must')
                obligations.append(simplified)
        
        return obligations[:6]  # Limit to 6 key obligations
    
    def identify_risks_and_warnings(self, text: str) -> List[str]:
        """Identify potential risks and important warnings"""
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        risks = []
        
        # Risk indicators
        risk_indicators = [
            'liability', 'penalty', 'fee', 'terminate', 'breach',
            'default', 'damages', 'dispute', 'arbitration', 'court'
        ]
        
        for sentence in sentences:
            if any(indicator in sentence.lower() for indicator in risk_indicators):
                # Highlight the risk
                risk_explanation = f"⚠️ {sentence}"
                risks.append(risk_explanation)
        
        return risks[:5]  # Limit to 5 main risks
    
    def calculate_readability(self, text: str) -> Dict[str, any]:
        """Calculate basic readability metrics"""
        words = text.split()
        sentences = [s for s in text.split('.') if s.strip()]
        
        if not sentences:
            return {"score": "N/A", "level": "Unable to calculate"}
        
        avg_words_per_sentence = len(words) / len(sentences)
        
        # Simple readability assessment
        if avg_words_per_sentence < 15:
            level = "Easy to read"
            score = "Good"
        elif avg_words_per_sentence < 25:
            level = "Moderate difficulty"
            score = "Fair"
        else:
            level = "Difficult to read"
            score = "Complex"
        
        return {
            "avg_words_per_sentence": round(avg_words_per_sentence, 1),
            "total_words": len(words),
            "total_sentences": len(sentences),
            "score": score,
            "level": level
        }
    
    def analyze_document(self, file_path: str) -> Dict:
        """Main analysis function"""
        print(f"🔍 Analyzing document: {file_path}")
        
        # Read document
        text = self.read_text_file(file_path)
        if not text:
            return {"error": "Could not read the document"}
        
        # Clean text
        cleaned_text = self.clean_text(text)
        print(f"📄 Document loaded: {len(cleaned_text.split())} words")
        
        # Perform analysis
        key_terms = self.extract_key_terms(cleaned_text)
        structure = self.analyze_document_structure(cleaned_text)
        summary = self.create_simple_summary(cleaned_text)
        obligations = self.extract_key_obligations(cleaned_text)
        risks = self.identify_risks_and_warnings(cleaned_text)
        readability = self.calculate_readability(cleaned_text)
        
        return {
            "document_info": {
                "file_path": file_path,
                "word_count": len(cleaned_text.split()),
                "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "key_terms": key_terms,
            "structure": structure,
            "plain_language_summary": summary,
            "key_obligations": obligations,
            "risks_and_warnings": risks,
            "readability": readability,
            "original_preview": cleaned_text[:300] + "..." if len(cleaned_text) > 300 else cleaned_text
        }
    
    def print_results(self, results: Dict):
        """Print formatted results"""
        print("\n" + "="*70)
        print("📋 LEGAL DOCUMENT ANALYSIS RESULTS")
        print("="*70)
        
        # Document info
        info = results.get("document_info", {})
        print(f"\n📄 Document: {info.get('file_path', 'Unknown')}")
        print(f"📊 Stats: {info.get('word_count', 0)} words")
        print(f"🕒 Analyzed: {info.get('analysis_date', 'Unknown')}")
        
        # Readability
        readability = results.get("readability", {})
        print(f"\n📖 READABILITY:")
        print(f"   Complexity: {readability.get('level', 'Unknown')}")
        print(f"   Average words per sentence: {readability.get('avg_words_per_sentence', 'N/A')}")
        
        # Key terms
        key_terms = results.get("key_terms", [])
        if key_terms:
            print(f"\n🎯 LEGAL TERMS FOUND:")
            for term in key_terms:
                print(f"   • {term}")
        
        # Summary
        summary = results.get("plain_language_summary", "")
        if summary:
            print(f"\n📝 PLAIN LANGUAGE SUMMARY:")
            print(f"   {summary}")
        
        # Key obligations
        obligations = results.get("key_obligations", [])
        if obligations:
            print(f"\n📋 KEY OBLIGATIONS:")
            for i, obligation in enumerate(obligations, 1):
                print(f"   {i}. {obligation}")
        
        # Risks and warnings
        risks = results.get("risks_and_warnings", [])
        if risks:
            print(f"\n⚠️  RISKS AND IMPORTANT WARNINGS:")
            for risk in risks:
                print(f"   {risk}")
        
        # Document structure
        structure = results.get("structure", {})
        sections = structure.get("sections", [])
        if sections:
            print(f"\n📑 DOCUMENT STRUCTURE:")
            print(f"   Sections found: {len(sections)}")
            for section in sections[:5]:  # Show first 5 sections
                print(f"   • {section}")
        
        print("\n" + "="*70)
        print("💡 TIP: This analysis uses rule-based processing.")
        print("   For more advanced AI analysis, set up OpenAI API or wait for model download.")
        print("="*70)


def create_sample_legal_text():
    """Create sample legal document for testing"""
    return """
    SERVICE AGREEMENT
    
    This Service Agreement is entered into between Company XYZ (Provider) and the Client.
    
    1. SERVICES
    Provider agrees to perform consulting services as described in Exhibit A. All services shall be 
    performed in a professional manner according to industry standards.
    
    2. PAYMENT TERMS
    Client agrees to pay Provider the fees outlined in Exhibit A. Payment is due within thirty (30) 
    days of invoice date. Late payments may incur a fee of 1.5% per month.
    
    3. CONFIDENTIALITY
    Both parties agree to maintain confidentiality of all shared information and not disclose 
    it to third parties without written consent.
    
    4. LIABILITY LIMITATION
    Provider's liability shall not exceed the total amount paid by Client under this Agreement. 
    Provider shall not be liable for indirect, incidental, or consequential damages.
    
    5. GOVERNING LAW
    This Agreement shall be governed by state law. Disputes shall be resolved through binding arbitration.
    
    6. TERMINATION
    Either party may terminate this Agreement with thirty (30) days written notice.
    """


def main():
    """Main function"""
    print("🏛️  Legal Document Demystifier - Demo Version")
    print("   (Works immediately without model downloads)")
    print("="*60)
    
    demystifier = SimpleLegalDemystifier()
    
    print("\n📋 Choose an option:")
    print("1. Analyze sample legal document")
    print("2. Analyze your own text file")
    print("3. Enter custom text")
    
    try:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            print("\n📄 Using sample legal document...")
            sample_text = create_sample_legal_text()
            
            sample_file = "sample_contract.txt"
            with open(sample_file, 'w', encoding='utf-8') as f:
                f.write(sample_text)
            
            results = demystifier.analyze_document(sample_file)
            demystifier.print_results(results)
            
            os.remove(sample_file)
            
        elif choice == "2":
            file_path = input("Enter path to your text file: ").strip()
            if os.path.exists(file_path):
                results = demystifier.analyze_document(file_path)
                demystifier.print_results(results)
                
                save = input("\nSave results to JSON file? (y/n): ").lower().strip()
                if save == 'y':
                    output_file = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    with open(output_file, 'w') as f:
                        json.dump(results, f, indent=2)
                    print(f"💾 Results saved to: {output_file}")
            else:
                print(f"❌ File not found: {file_path}")
        
        elif choice == "3":
            print("\n📝 Enter your legal text (press Enter twice when done):")
            lines = []
            empty_lines = 0
            while empty_lines < 2:
                line = input()
                if line == "":
                    empty_lines += 1
                else:
                    empty_lines = 0
                lines.append(line)
            
            custom_text = "\n".join(lines[:-2])  # Remove the two empty lines
            if custom_text.strip():
                temp_file = "temp_text.txt"
                with open(temp_file, 'w', encoding='utf-8') as f:
                    f.write(custom_text)
                
                results = demystifier.analyze_document(temp_file)
                demystifier.print_results(results)
                
                os.remove(temp_file)
            else:
                print("❌ No text entered.")
        
        else:
            print("❌ Invalid choice.")
    
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()