import PIL.Image
# import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv


# Initialize Gemini-Pro 
load_dotenv(find_dotenv())
genai.configure()
# model = genai.GenerativeModel('gemini-1.0-pro-latest')
img = PIL.Image.open('img.jpg')
model = genai.GenerativeModel('gemini-pro-vision')
response = model.generate_content(img)

response = model.generate_content(["Write a short, engaging blog post based on this picture. It should include a description of the meal in the photo and talk about my journey meal prepping.", img])
response.resolve()
print(response.text)