from langchain.document_loaders import PyMuPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path
from dotenv import load_dotenv
import os
from pinecone import Pinecone, ServerlessSpec

from langchain_community.document_loaders import PyMuPDFLoader, DirectoryLoader
from langchain_community.embeddings import HuggingFaceEmbeddings


load_dotenv()



# Extract data from the PDF file
def load_pdf_file(data):
    data_path = Path(data)
    if not data_path.exists():
        raise ValueError(f"Path {data_path} does not exist!")
        
    loader = DirectoryLoader(
        str(data_path),  # Convert to string for compatibility
        glob="*.pdf",
        loader_cls=PyMuPDFLoader
    )
    return loader.load()


def load_pdf_file_2(data):
    loader = DirectoryLoader(
        data,
        glob="*.pdf",
        loader_cls=PyMuPDFLoader
    )

    document = loader.load()

    return document


# Spliting the data into test chunks
def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    text_chunk = text_splitter.split_documents(extracted_data)
    return text_chunk


# Download the embedding from hugging face
def download_hugging_face_embedding():
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    return embeddings
