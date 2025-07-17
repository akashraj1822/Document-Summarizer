import streamlit as st
from transformers import pipeline
import fitz
import docx
import re
import torch

def load_summarizer():
    return pipeline("summarization", model="csebuetnlp/mT5_multilingual_XLSum", torch_dtype=torch.float32)

summarizer = load_summarizer()

def clean_text(text):
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    return text

def extract_text(file):
    file_type = file.name.split('.')[-1]
    if file_type == "txt":
        return file.read().decode("utf-8")
    elif file_type == "pdf":
        pdf = fitz.open(stream=file.read(), filetype="pdf")
        return "\n".join(page.get_text() for page in pdf)
    elif file_type == "docx":
        doc = docx.Document(file)
        return "\n".join(para.text for para in doc.paragraphs)
    else:
        return ""

st.set_page_config(page_title="Indic Document Summarizer + Q&A", layout="centered")
st.title("Indic Document Summarizer + Q&A")
st.markdown("Upload a `.txt`, `.pdf`, or `.docx` file in English or Indic languages. Get a summary and ask questions.")

uploaded_file = st.file_uploader("Upload your document", type=["txt", "pdf", "docx"])

if uploaded_file:
    with st.spinner("Reading file..."):
        doc_text = extract_text(uploaded_file)
        doc_text = clean_text(doc_text)

    if len(doc_text.strip()) < 20:
        st.warning("The file doesn't contain enough readable text.")
    else:
        if st.button("Generate Summary"):
            with st.spinner("Summarizing..."):
                try:
                    result = summarizer(doc_text[:1000])[0]
                    st.subheader("Summary:")
                    st.markdown(result['summary_text'])
                except Exception as e:
                    st.error(f"Summarization failed: {e}")

        user_question = st.text_input("Ask a question about the document:")
        if user_question and st.button("Get Answer"):
            with st.spinner("Generating answer..."):
                try:
                    qa_prompt = f"{doc_text[:1000]}\n\nQuestion: {user_question}\n\nAnswer:"
                    answer = summarizer(qa_prompt)[0]['summary_text']
                    st.subheader("Answer:")
                    st.markdown(answer)
                except Exception as e:
                    st.error(f"Failed to generate answer: {e}")
