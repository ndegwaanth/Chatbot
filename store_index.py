from src.helper import load_pdf_file_2, text_split, download_hugging_face_embedding
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')


# Get the current directory and construct the Data path
data_dir = Path(__file__).parent / "research/Data"

print(f"Looking for PDFs in: {data_dir}")

# Verify the directory exists
if not data_dir.exists():
    raise FileNotFoundError(f"Data directory not found at: {data_dir}")

extracted_data = load_pdf_file_2(data=data_dir)


text_chunk = text_split(extracted_data)
# print(f"Lenght of text extracted {len(text_chunk)}")


embeddings = download_hugging_face_embedding()



from pinecone import Pinecone, ServerlessSpec

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Create an index if it doesn't exist
if "chatbot" not in pc.list_indexes():
    pc.create_index(
        name="chatbot",
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

# Connect to the index
index = pc.Index("chatbot")

# print("Pinecone index setup complete!")


# Embed each chunk and insert the embeddings into pinecone index
sec_search = PineconeVectorStore.from_documents(
    documents=text_chunk,
    index_name = "chatbot",
    embedding=embeddings
)