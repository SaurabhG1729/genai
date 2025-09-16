# Legal Document Demystifier - Student Project

## Quick Start Guide

### 1. Install Required Packages

Choose one of these options:

#### Option A: OpenAI API (Paid, but very good results)
```bash
pip install openai PyPDF2
```
Then set your API key:
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="your_api_key_here"

# Or add to your environment variables permanently
```

#### Option B: Hugging Face (Free, runs locally)
```bash
pip install transformers torch PyPDF2
```

#### Option C: Install everything
```bash
pip install -r requirements.txt
```

### 2. Run the Project
```bash
python main.py
```

### 3. Test Options

The program offers three ways to test:

1. **Built-in Sample**: Uses a sample legal document (easiest for testing)
2. **Your Own File**: Upload a PDF or text file of a legal document
3. **Custom Text**: Paste legal text directly

### 4. What You'll Get

The program will output:
- **Document Summary**: Simplified explanation of what the document means
- **Key Points**: Most important things to know
- **Potential Risks**: Things to watch out for
- **Legal Terms**: Important legal terms found in the document

### 5. Example Output

```
📋 LEGAL DOCUMENT ANALYSIS RESULTS
============================================================

📄 Document: sample_legal_document.txt
📊 Stats: 245 words, 1456 characters
🕒 Analyzed: 2024-01-15 14:30:22

🎯 KEY LEGAL TERMS FOUND:
  • Service Agreement
  • confidential information
  • liability
  • governing law
  • arbitration

🤖 AI ANALYSIS RESULTS:

📝 SUMMARY:
This is a contract between a service provider and a client. The provider will do consulting work, the client will pay within 30 days, both parties must keep information confidential, and if there are problems, they'll be solved through arbitration rather than court.

🎯 KEY POINTS:
1. Services must be performed professionally
2. Payment is due within 30 days
3. Late payments incur 1.5% monthly fees
4. Both parties must keep information confidential
5. Either party can end the contract with 30 days notice

⚠️ POTENTIAL RISKS/IMPORTANT NOTES:
- Late payment fees of 1.5% per month can add up quickly
- Disputes must be resolved through arbitration, not court
- Provider's liability is limited to the amount you paid
- Either party can terminate with just 30 days notice
```

### 6. Troubleshooting

**"OpenAI API key not found"**
- Set the OPENAI_API_KEY environment variable
- Or use the Hugging Face option instead

**"Import errors"**
- Install the required packages: `pip install openai transformers torch PyPDF2`

**"Model loading takes too long"**
- This is normal for Hugging Face models on first run
- The model downloads and caches locally

**"PDF reading errors"**
- Make sure the PDF contains text (not just images)
- Try converting to .txt file first

### 7. Next Steps

Once you have this working, you can:
- Test with different types of legal documents
- Experiment with the AI prompts in the code
- Add new features like document comparison
- Create a simple web interface with Streamlit

### 8. Educational Value

This project teaches:
- Working with AI APIs and local models
- Text processing and natural language processing
- File handling and document parsing
- Error handling and user interface design
- Practical applications of AI in real-world problems

## File Structure
```
genai/
├── main.py           # Main application
├── requirements.txt  # Package dependencies
└── README.md        # This file
```