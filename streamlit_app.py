import os
import tempfile
import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitte
rfrom langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import HuggingFaceHub
# --- SETUP ---
load_dotenv()
hf_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")
st.set_page_config(page_title="AI-Powered Research Paper Summarizer & Comparator", layout="wide")

st.title("📚 AI-Powered Research Paper Summarizer & Comparator")
st.markdown("Upload research papers to get AI-generated summaries and comparisons.")

uploaded_files = st.file_uploader("📎 Upload PDFs or Text Files", type=["pdf", "txt", "docx"], accept_multiple_files=True)

if not hf_key:
    st.error("❌ Hugging Face API key not found. Add it to your .env file.")
    st.stop()

def load_documents(uploaded_files):
    docs = []
    for file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file.name) as tmp:
            tmp.write(file.read())
            path = tmp.name
        if file.name.endswith(".pdf"):
            docs.extend(PyPDFLoader(path).load())
        elif file.name.endswith(".txt"):
            docs.extend(TextLoader(path).load())
        elif file.name.endswith(".docx"):
            docs.extend(UnstructuredWordDocumentLoader(path).load())
    return docs

if uploaded_files:
    st.info("🔍 Processing uploaded papers...")
    documents = load_documents(uploaded_files)

    # --- Split and Embed ---
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    
    # --- Load summarization LLM ---
    summarizer = HuggingFaceHub(
        repo_id="facebook/bart-large-cnn",
        model_kwargs={"temperature": 0.3, "max_length": 300},
        huggingfacehub_api_token=hf_key
    )

    # --- Summarization Section ---
    st.subheader("🧾 Summaries")
    for i, doc in enumerate(uploaded_files, start=1):
        query = f"Summarize the main contributions and findings of {doc.name}"
        context_docs = retriever.get_relevant_documents(query)
        combined_text = "\n".join(d.page_content for d in context_docs)
        summary = summarizer(combined_text)
        st.markdown(f"**📄 {doc.name}**")
        st.write(summary)
        st.divider()

    # --- Comparison Section ---
    if len(uploaded_files) >= 2:
        st.subheader("⚖️ Comparative Analysis")
        compare_query = "Compare these research papers. Highlight similarities, differences, and contradictions."
        compare_context = "\n\n".join([d.page_content for d in documents])
        comparison = summarizer(compare_context)
        st.success("### 🔬 Comparison Summary")
        st.write(comparison)
else:
    st.info("📂 Upload research papers to begin.")
