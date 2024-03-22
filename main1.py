import streamlit as st
import textwrap
import google.generativeai as genai
import PIL.Image

# Function to display text as Markdown
def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ')

# Configure Google API key
genai.configure(api_key="AIzaSyCYzxQPSdTuhQ6WAeq8XosSKYRz-9cxuNA")

# Main function to generate content
def generate_content(prompt, model_name, image=None):
    model = genai.GenerativeModel(model_name)
    if model_name == "gemini-pro-vision":
        response = model.generate_content([prompt, image])
    else:
        response = model.generate_content(prompt)
    return response

# Streamlit UI
st.title("Jawad's Chat Bot")
st.sidebar.title("Settings")
model_name = st.sidebar.selectbox("Select Model", ["gemini-pro", "gemini-pro-vision"])
prompt = st.text_input("Enter Prompt", "What is the meaning of life?")

if model_name == "gemini-pro-vision":
    image_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
else:
    image_file = None

generate_button = st.button("Generate")

if generate_button:
    if model_name == "gemini-pro-vision" and image_file is None:
        st.write("Please upload an image.")
    else:
        st.write("Generating content...")
        if model_name == "gemini-pro-vision":
            image = PIL.Image.open(image_file)
            response = generate_content(prompt, model_name, image)
            if response and hasattr(response, 'text'):
                response_text = response.text
                st.markdown(to_markdown(response_text))
            elif response and hasattr(response, 'image'):
                st.image(response.image, caption="Generated Image", use_column_width=True)
            else:
                st.write("Failed to generate content. Please try again.")
        else:
            response = generate_content(prompt, model_name)
            if response and hasattr(response, 'text'):
                response_text = response.text
                st.markdown(to_markdown(response_text))
            else:
                st.write("Failed to generate content. Please try again.")

st.sidebar.text("Powered by Gemini AI")
