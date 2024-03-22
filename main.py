import streamlit as st
import requests
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv

# Initialize Gemini-Pro
load_dotenv(find_dotenv())
genai.configure()
model = genai.GenerativeModel('gemini-1.0-pro-latest')

# Gemini uses 'model' for assistant; Streamlit uses 'assistant'
def role_to_streamlit(role):
    if role == "model":
        return "assistant"
    else:
        return role

# Add a Gemini Chat history object to Streamlit session state
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

def query_ocr(data):
    API_URL = "https://api-inference.huggingface.co/models/microsoft/trocr-base-handwritten"
    headers = {"Authorization": "Bearer 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"}
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

def main():
    st.title("Jawad's Chat Bot")

    # Add a text input box
    text_input = st.text_input("Feel free to ask any question:", "")

    # Add an image insertion button
    uploaded_file = st.file_uploader("Attach an image...", type=["jpg", "png"])

    # Display chat messages from history above current input box
    for message in st.session_state.chat.history[1:]:
        with st.chat_message(role_to_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    if text_input:
        # Display user's input message
        with st.chat_message("user"):
            st.markdown(text_input)

        # Send user input to Gemini and read the response
        response = st.session_state.chat.send_message(text_input)

        # Display Gemini's response
        with st.chat_message("assistant"):
            st.markdown(response.text)

    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        st.write("")
        st.write("Processing...")

        # Read contents of the uploaded file
        file_contents = uploaded_file.read()

        # Perform OCR
        ocr_output = query_ocr(file_contents)

        if "error" in ocr_output:
            st.error("Error occurred during OCR: " + ocr_output["error"])
        else:
            st.write("OCR Result:")
            st.text('\n'.join(ocr_output))  # Display OCR output as text

if __name__ == "__main__":
    main()
