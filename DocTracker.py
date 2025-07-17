import streamlit as st
from transformers import pipeline
import fitz  
import docx

@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="t5-small")

summarizer = load_summarizer()

def extract_text(file):
    if file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    elif file.name.endswith(".pdf"):
        pdf = fitz.open(stream=file.read(), filetype="pdf")
        return "\n".join([page.get_text() for page in pdf])
    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    return ""

st.set_page_config(page_title="Indic Doc Summarizer+Q&A", layout="centered")
st.title("Indic Document Summarizer + Q&A")

st.markdown("Upload a `.txt`, `.pdf`, or `.docx` file in English and get a summary and ask questions.")

uploaded_file = st.file_uploader("Upload your document", type=["txt", "pdf", "docx"])

if uploaded_file:
    with st.spinner("Reading file..."):
        doc_text = extract_text(uploaded_file)

    if len(doc_text.strip()) < 20:
        st.warning("The file doesn't contain enough readable text.")
    else:
        if st.button("Generate Summary"):
            with st.spinner("Summarizing..."):
                try:
                    result = summarizer(doc_text[:4000], max_length=100, min_length=30)[0]
                    st.success("Summary:")
                    st.markdown(result['summary_text'])
                except Exception as e:
                    st.error(f"Failed to summarize: {e}")

        user_question = st.text_input("Ask a question about the document:")
        if user_question and st.button("Get Answer"):
            with st.spinner("Generating answer..."):
                try:
                    qa_prompt = f"{doc_text[:4000]}\n\nQuestion: {user_question}\n\nAnswer:"
                    answer = summarizer(qa_prompt, max_length=100, min_length=30)[0]['summary_text']
                    st.success("Answer:")
                    st.markdown(answer)
                except Exception as e:
                    st.error(f"Failed to answer: {e}")
