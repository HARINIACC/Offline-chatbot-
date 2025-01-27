# Offline-chatbot-
Interactive Document Chat Assistant

This project allows users to upload a PDF document and interact with an AI assistant to ask questions about the content of the document. The assistant ensures accurate, concise, and document-based responses.

**Features**

Upload PDF Documents: Easily upload any PDF document.

AI-Powered Chat: Ask questions about the document's content and receive intelligent answers.

Accurate Responses: The assistant bases its responses strictly on the document's information.

Interactive UI: User-friendly interface built with Streamlit.

**Prerequisites**

Ensure you have the following installed:

Python 3.8 or later

Required Python libraries:

streamlit

marker

llama-index

qdrant-client

**You can install the dependencies with:**

pip install streamlit marker llama-index qdrant-client

**How to Run**

Clone the Repository:

git clone <repository_url>
cd <repository_folder>

Run the Streamlit App:

streamlit run app.py

**Upload a PDF:**

Use the file uploader to upload a PDF document.

**Start Chatting:**

Type your questions in the input box and press Enter to receive responses.

Code Overview

Core Components

**PDF Upload**:

Users upload a PDF file via the Streamlit interface.

**Text Extraction:**

Extracts text from the uploaded PDF using marker library.

**Document Parsing:**

Converts extracted text into a format suitable for querying.

**Chat Engine:**

Uses llama-index and Ollama for generating responses.

Embeddings are created with HuggingFaceEmbedding.

**Vector Store:**

Stores document embeddings in a Qdrant-based vector store for efficient querying.

Example Workflow

Upload a PDF document.

Ask a question, e.g., "What does the document say about topic X?"

View the bot's response.

Troubleshooting

Dependencies Issue: Ensure all required libraries are installed. Use:

pip install -r requirements.txt

Error with PDF Upload: Check the file type and ensure it's a valid PDF.

Slow Response: Ensure you have a stable internet connection for LLM-based queries.

Notes

The assistant only answers based on the content of the uploaded PDF.

Temporary files are cleaned up after processing.

Author

Harini

Feel free to reach out for feedback or contributions!

