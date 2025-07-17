# Indic Document Summarizer + Q&A

This is a simple AI-powered Streamlit app that allows you to:

- Upload `.pdf`, `.docx`, or `.txt` documents written in Indian languages (like Hindi, Tamil, Telugu, Bengali, English)
- Get a clean summary of the document
- Ask questions based on the document and get answers using AI

Built with:
- Streamlit
- Hugging Face Transformers
- `csebuetnlp/mT5_multilingual_XLSum` model

---

## How to Use

1. Upload a `.txt`, `.pdf`, or `.docx` file.
2. Choose the language of your document (Hindi, Tamil, etc.)
3. Click "Generate Summary" to get a summarized version.
4. Type a question and click "Get Answer" to extract insights from the document.

---

## Setup Locally

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
pip install -r requirements.txt
streamlit run DocTracker.py
