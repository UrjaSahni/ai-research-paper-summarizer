# 📚 AI Research Paper Summarizer & Comparator

An AI-powered web application that helps researchers and students quickly understand and compare research papers using state-of-the-art NLP models from Hugging Face.

## ✨ Features

- 📄 **Multiple File Format Support**: Upload PDF, DOCX, PPTX, TXT, and MD files
- 🤖 **AI-Powered Summarization**: Uses Hugging Face's BART model for high-quality summaries
- 📊 **Document Comparison**: Compare multiple research papers (coming soon)
- 💾 **Export Results**: Download summaries for offline use
- 🔒 **Privacy-Focused**: All processing happens on your machine - no data storage

## 🚀 Live Demo

https://ai-research-paper-summarizer-evyrkrdny4ruogvf3iptz2.streamlit.app/

## 📸 Screenshots

_Coming soon_

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI Model**: Hugging Face Transformers (facebook/bart-large-cnn)
- **File Processing**: PyPDF2, python-docx, python-pptx
- **Language**: Python 3.8+

## 💻 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Hugging Face API key ([Get one here](https://huggingface.co/))

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/UrjaSahni/ai-research-paper-summarizer.git
cd ai-research-paper-summarizer
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the app**
```bash
streamlit run streamlit_app.py
```

4. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - Enter your Hugging Face API key in the sidebar
   - Upload your research papers and start summarizing!

## 🔑 Getting Your Hugging Face API Key

1. Go to [Hugging Face](https://huggingface.co/)
2. Sign up or log in to your account
3. Navigate to Settings → Access Tokens
4. Click "New token" and create a token with read permissions
5. Copy the token and paste it in the app's sidebar

## 📝 Usage

### Summarizing Documents

1. **Upload Files**: Click on the file uploader and select one or more documents
2. **Enter API Key**: Paste your Hugging Face API key in the sidebar
3. **View Summaries**: The app will automatically process and display summaries
4. **Check Stats**: See word count reduction and processing metrics

### Supported File Formats

- **PDF**: Research papers, articles, reports
- **DOCX**: Microsoft Word documents
- **PPTX**: PowerPoint presentations
- **TXT**: Plain text files
- **MD**: Markdown files

## 🎯 Use Cases

- 🎓 **Students**: Quickly understand research papers for assignments
- 🔬 **Researchers**: Get overviews of papers before deep reading
- 💼 **Professionals**: Summarize technical documents and reports
- 📚 **Literature Review**: Process multiple papers efficiently

## 📁 Project Structure

```
ai-research-paper-summarizer/
├── streamlit_app.py       # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── LICENSE               # MIT License
└── .gitignore            # Git ignore file
```

## 🚀 Deployment on Streamlit Cloud

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Sign in with GitHub
4. Click "New app"
5. Select your forked repository
6. Set `streamlit_app.py` as the main file
7. Click "Deploy"!

## 🤝 Contributing

Contributions are welcome! Feel free to:

- 🐛 Report bugs
- 💡 Suggest new features
- 🛠️ Submit pull requests

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👏 Acknowledgments

- [Hugging Face](https://huggingface.co/) for providing amazing AI models
- [Streamlit](https://streamlit.io/) for the intuitive web framework
- The open-source community for various libraries used

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Made with ❤️ using Streamlit and Hugging Face 🤗**
