from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embedding
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os


load_dotenv()


app = Flask(__name__)

# Retrieve the API key from the environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')

embeddings = download_hugging_face_embedding()

# Loading Existing index
sec_search = PineconeVectorStore.from_existing_index(
    index_name="chatbot",
    embedding=embeddings
)

# Initialize OpenAI with the API key
llm = OpenAI(api_key=OPENAI_API_KEY, temperature=0.4, max_tokens=500)

retriver = sec_search.as_retriever(sec_search="similarity", search_kwargs={"k":3})


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}")
    ]
)


question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriver, question_answer_chain)


@app.route("/")
def index():
    return render_template("chatbot.html")


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form['msg']
    input = msg
    print(input)

    response = rag_chain.invoke({"input": msg})
    print("Response : ", response(["answer"]))
    return str(response["answer"])


if __name__ == "__main__":
    app.run(debug=True)