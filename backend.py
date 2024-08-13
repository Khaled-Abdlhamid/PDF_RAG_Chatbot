from fastapi import FastAPI, File, UploadFile, Form
import PyPDF2
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceHubEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
import os

huggingface_api = 'hf_QrAltZgfqZQqALKSZxindDfwWJSAFPyNLdWmbUA'
os.environ["HUGGINGFACEHUB_API_TOKEN"] = huggingface_api

google_gemini_api_key = 'AIZasyBVtEZxLAJWZ9D6G2giC55nEMN5PZ-psKn'
genai.configure(api_key=google_gemini_api_key)

app = FastAPI()

# Global variables
conversation_chain = None

# Function to read PDF
def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Initialize the Google Gemini LLM
def initialize_google_gemini_llm():
    return ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=google_gemini_api_key ,temperature=0.7)

@app.post("/process_pdf/")
async def process_pdf(pdf_file: UploadFile = File(...)):
    global conversation_chain
    
    # Read PDF
    raw_text = read_pdf(pdf_file.file)

    # Split text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_text(raw_text)

    # Initialize Google Gemini LLM and embeddings
    llm = initialize_google_gemini_llm()
    embeddings = HuggingFaceHubEmbeddings()

    # Create vector store
    vectorstore = FAISS.from_texts(texts, embeddings)

    # Create conversation chain
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )

    return {"message": "PDF processed successfully!"}

@app.post("/chat/")
async def chat(prompt: str = Form(...)):
    if conversation_chain is None:
        return {"error": "PDF not processed yet. Please upload a PDF first."}
    
    response = conversation_chain({"question": f"Explain in detail: {prompt}"})
    return {"response": response['answer']}
