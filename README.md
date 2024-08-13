# PDF RAG Chatbot

This project is a simple PDF Retrieval-Augmented Generation (RAG) chatbot built using Streamlit for the frontend and FastAPI for the backend. The chatbot processes a PDF file, creates a vector store for the PDF's text, and allows users to ask questions about the content of the PDF. The chatbot uses the Google Gemini LLM via the `langchain_google_genai` package for generating detailed responses.

## Project Structure

- `backend.py`: The FastAPI backend that handles PDF processing and chat functionalities.
- `frontend.py`: The Streamlit frontend that provides the user interface and interacts with the backend.

## How to Run?
- Start the FastAPI Backend : uvicorn backend:app --reload
- Start the Streamlit Frontend : streamlit run frontend.py
- Upload a PDF File
- Ask Questions 


**PS: please don't forget to update gemeni and huggingface APIs :)**