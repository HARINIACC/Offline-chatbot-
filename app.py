import streamlit as st
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered
from pathlib import Path
from llama_index.core import StorageContext, Document
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import Settings, VectorStoreIndex
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import qdrant_client

# Page configuration
st.set_page_config(page_title="Document Chat Assistant", layout="centered")
st.title("\U0001F4D6 Interactive Document Chat Assistant")



# File uploader
uploaded_file = st.file_uploader("Upload your PDF document", type="pdf")

# Function to initialize the chat engine
def initialize_chat_engine(file_path):
    # Initialize converter
    converter = PdfConverter(artifact_dict=create_model_dict())
    rendered = converter(file_path)
    text, _, _ = text_from_rendered(rendered)

    # Create document and parse
    doc = Document(text=text, metadata={"name": file_path})
    parser = MarkdownNodeParser()
    nodes = parser.get_nodes_from_documents([doc])
    documents = [Document(text=t.text, metadata=t.metadata) for t in nodes]

    # Setup LLM and embeddings
    SYSTEM_PROMPT = """
    You are an AI assistant that answers questions based on the provided source document.
    Ensure your responses are accurate, concise, and derived only from the document content.
    """

    llm = Ollama(model="mistral", request_timeout=120.0)
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

    Settings.llm = llm
    Settings.embed_model = embed_model

    # Setup vector store
    client = qdrant_client.QdrantClient(location=":memory:")
    vector_store = QdrantVectorStore(
        collection_name="document_chat",
        client=client,
        enable_hybrid=True,
        batch_size=20,
    )

    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

    # Return chat engine
    return index.as_chat_engine(
        query_engine=index.as_query_engine(),
        chat_mode="context",
        system_prompt=SYSTEM_PROMPT,
        llm=llm
    )

# Main app logic
if uploaded_file:
    if "chat_engine" not in st.session_state:
        with st.spinner("Processing your document..."):
            # Save the uploaded file temporarily
            temp_path = Path("temp.pdf")
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getvalue())

            # Initialize chat engine and store in session state
            st.session_state.chat_engine = initialize_chat_engine(str(temp_path))

            # Clean up temporary file
            temp_path.unlink()

    # Conversational bot interface
    st.markdown("### Engage in a conversation about your document")

    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    user_input = st.text_input("Your question:", placeholder="Type your question here and press Enter")

    if user_input:
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(user_input)
            st.session_state.conversation.append((user_input, response.response))

    for question, answer in st.session_state.conversation:
        st.markdown(f"**You:** {question}")
        st.markdown(f"**Bot:** {answer}")
else:
    st.info("Please upload a PDF document to start the conversation.")
