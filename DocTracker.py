import streamlit as st
from transformers import pipeline
import fitz
import docx
import re

@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="t5-small")

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

def trim_text(text, max_words=300):
    words = text.split()
    return ' '.join(words[:max_words])

st.set_page_config(page_title="English Document Summarizer + Q&A", layout="centered")
st.title("English Document Summarizer + Q&A")
st.markdown("Upload a `.txt`, `.pdf`, or `.docx` file in English. Get a concise summary and ask questions about its content.")

uploaded_file = st.file_uploader("Upload your document", type=["txt", "pdf", "docx"])

if uploaded_file:
    with st.spinner("Reading and processing document..."):
        doc_text = extract_text(uploaded_file)
        doc_text = clean_text(doc_text)
        doc_text = trim_text(doc_text)

    if len(doc_text.strip()) < 20:
        st.warning("The file doesn't contain enough readable text.")
    else:
        if st.button("Generate Summary"):
            with st.spinner("Summarizing..."):
                try:
                    input_text = "summarize: " + doc_text
                    result = summarizer(input_text, max_length=120, min_length=30, do_sample=False)[0]
                    st.subheader("Summary:")
                    st.markdown(result['summary_text'])
                except Exception as e:
                    st.error(f"Summarization failed: {e}")

        user_question = st.text_input("Ask a question about the document:")
        if user_question and st.button("Get Answer"):
            with st.spinner("Generating answer..."):
                try:
                    qa_prompt = f"summarize: {doc_text}\n\nQuestion: {user_question}\n\nAnswer:"
                    answer = summarizer(qa_prompt, max_length=120, min_length=30, do_sample=False)[0]['summary_text']
                    st.subheader("Answer:")
                    st.markdown(answer)
                except Exception as e:
                    st.error(f"Failed to generate answer: {e}")
