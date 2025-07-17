# English Document Summarizer + Q&A

This is a simple AI-powered Streamlit web app that allows you to:

- Upload `.pdf`, `.docx`, or `.txt` documents written in **English**
- Get a concise summary of the document
- Ask questions based on the document and receive intelligent answers using AI

---

## Built With

- Streamlit – for UI and web deployment
- Hugging Face Transformers – for summarization and Q&A
- Model Used: `t5-small` (via Hugging Face)

---

## Features

- Supports file types: `.txt`, `.pdf`, `.docx`
- Cleans and trims the text for efficient summarization
- Uses a pre-trained `t5-small` model for summarization and basic Q&A
- Minimal, fast, and lightweight – great for English documents

---

## How to Use

1. Upload an English `.txt`, `.pdf`, or `.docx` file.
2. Click "Generate Summary" to view the summary.
3. Type a question about the document.
4. Click "Get Answer" to receive a response from the model.

---

## Setup Locally

Clone the repository and run the app on your local machine.

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
pip install -r requirements.txt
streamlit run DocTracker.py
