import streamlit as st
import requests

backend_url = "http://localhost:8000"

st.title("PDF RAG Chatbot")

pdf_file = st.file_uploader("Upload a PDF file", type="pdf")

if pdf_file is not None:
    with st.spinner("Processing PDF..."):
        files = {'pdf_file': pdf_file}
        response = requests.post(f"{backend_url}/process_pdf/", files=files)
        
    if response.status_code == 200:
        st.success("PDF processed successfully!")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("What would you like to know about the PDF?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                chat_response = requests.post(f"{backend_url}/chat/", data={"prompt": prompt})
                response_text = chat_response.json().get("response", "Error: No response")
                st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})

    else:
        st.error("Failed to process PDF.")
else:
    st.write("Please upload a PDF file to start.")
