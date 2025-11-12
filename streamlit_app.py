import streamlit as st
import os
from transformers import pipeline
from PyPDF2 import PdfReader
import docx
from pptx import Presentation
import io

# Page config
st.set_page_config(
    page_title="AI Research Paper Summarizer",
    page_icon="📚",
    layout="wide"
)

# Title and description
st.title("📚 AI Research Paper Summarizer & Comparator")
st.markdown("""
This app uses Hugging Face models to summarize and compare research papers.
Upload your documents (PDF, DOCX, PPTX, TXT, MD) and get AI-powered summaries.
""")

# Sidebar for API key
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Hugging Face API Key", type="password", help="Enter your HF API key")
    st.markdown("---")
    st.markdown("""
    ### Features:
    - 📄 Multiple file format support
    - 🤖 AI-powered summarization
    - 📊 Document comparison
    - 💾 Export results
    """)

# Helper functions
def extract_text_from_pdf(file):
    """Extract text from PDF file"""
    try:
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_text_from_docx(file):
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"

def extract_text_from_pptx(file):
    """Extract text from PPTX file"""
    try:
        prs = Presentation(file)
        text = ""
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text += shape.text + "\n"
        return text
    except Exception as e:
        return f"Error reading PPTX: {str(e)}"

def extract_text_from_txt(file):
    """Extract text from TXT/MD file"""
    try:
        text = file.read().decode('utf-8')
        return text
    except Exception as e:
        return f"Error reading file: {str(e)}"

def get_file_text(file):
    """Route to appropriate text extraction function"""
    if file.name.endswith('.pdf'):
        return extract_text_from_pdf(file)
    elif file.name.endswith('.docx'):
        return extract_text_from_docx(file)
    elif file.name.endswith('.pptx'):
        return extract_text_from_pptx(file)
    elif file.name.endswith(('.txt', '.md')):
        return extract_text_from_txt(file)
    else:
        return "Unsupported file format"

# Main app
tab1, tab2, tab3 = st.tabs(["📄 Upload & Summarize", "🔍 Compare Documents", "ℹ️ About"])

with tab1:
    st.header("Upload Documents for Summarization")
    
    uploaded_files = st.file_uploader(
        "Choose files (PDF, DOCX, PPTX, TXT, MD)",
        accept_multiple_files=True,
        type=['pdf', 'docx', 'pptx', 'txt', 'md']
    )
    
    if uploaded_files and api_key:
        try:
            # Initialize summarizer
            summarizer = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                token=api_key
            )
            
            for idx, file in enumerate(uploaded_files):
                st.subheader(f"📖 {file.name}")
                
                with st.spinner(f"Processing {file.name}..."):
                    # Extract text
                    text = get_file_text(file)
                    
                    if text.startswith("Error"):
                        st.error(text)
                        continue
                    
                    # Show original text (truncated)
                    with st.expander("View Original Text (First 500 chars)"):
                        st.text(text[:500] + "..." if len(text) > 500 else text)
                    
                    # Chunk text for summarization (BART has max 1024 tokens)
                    max_chunk_size = 1000
                    chunks = [text[i:i+max_chunk_size] for i in range(0, len(text), max_chunk_size)]
                    
                    # Summarize each chunk
                    summaries = []
                    for i, chunk in enumerate(chunks[:5]):  # Limit to first 5 chunks
                        if len(chunk.split()) > 50:  # Only summarize if chunk is substantial
                            summary = summarizer(chunk, max_length=130, min_length=30, do_sample=False)
                            summaries.append(summary[0]['summary_text'])
                    
                    # Combine summaries
                    final_summary = " ".join(summaries)
                    
                    # Display summary
                    st.markdown("**Summary:**")
                    st.info(final_summary)
                    
                    # Stats
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Original Words", len(text.split()))
                    with col2:
                        st.metric("Summary Words", len(final_summary.split()))
                    with col3:
                        reduction = round((1 - len(final_summary.split())/len(text.split())) * 100, 1)
                        st.metric("Reduction", f"{reduction}%")
                
                st.markdown("---")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("Please check your API key and try again.")
    
    elif uploaded_files and not api_key:
        st.warning("⚠️ Please enter your Hugging Face API key in the sidebar to continue.")
    else:
        st.info("👆 Upload files to get started!")

with tab2:
    st.header("Compare Multiple Documents")
    st.markdown("""
    Upload multiple documents to compare their content, identify:
    - Common themes
    - Unique contributions
    - Contradictions
    """)
    
    if uploaded_files and len(uploaded_files) >= 2:
        st.success(f"✅ {len(uploaded_files)} documents ready for comparison")
        st.info("Comparison feature: Extract key points from each document and highlight differences.")
    else:
        st.warning("Upload at least 2 documents in the 'Upload & Summarize' tab for comparison.")

with tab3:
    st.header("About This App")
    st.markdown("""
    ### 🎯 Purpose
    This AI-powered tool helps researchers and students quickly understand and compare research papers.
    
    ### 🛠️ Technology Stack
    - **Frontend**: Streamlit
    - **AI Model**: Hugging Face Transformers (BART)
    - **File Processing**: PyPDF2, python-docx, python-pptx
    
    ### 📝 How to Use
    1. Enter your Hugging Face API key in the sidebar
    2. Upload your research papers (PDF, DOCX, PPTX, TXT, MD)
    3. Get AI-generated summaries instantly
    4. Compare multiple documents (coming soon)
    
    ### 🔑 Get Your API Key
    1. Go to [Hugging Face](https://huggingface.co/)
    2. Sign up/Login
    3. Go to Settings → Access Tokens
    4. Create a new token
    
    ### 👨‍💻 Developer
    Built with ❤️ using Streamlit and Hugging Face
    """)
    
    st.markdown("---")
    st.markdown("**Note**: This app processes documents locally. Your data is not stored.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center'>Made with Streamlit • Powered by Hugging Face 🤗</div>",
    unsafe_allow_html=True
)
