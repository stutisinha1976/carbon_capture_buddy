from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load Google API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load the model and get responses
def get_gemini_response(input_text, image=None):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Check if the question is about carbon footprint
    if "carbon footprint" in input_text.lower():
        input_text = f"Provide a rough average value for the carbon footprint for the following object or activity: {input_text}, if the carbon content is more than a healthy amount, suggest an alternative. "

    # Generate the response based on input and image
    if input_text:
        response = model.generate_content([input_text, image] if image else [input_text])
    else:
        response = model.generate_content(image)
    
    return response.text

# Initialize Streamlit app
st.set_page_config(page_title="Carbon Footprint Demo",page_icon="leaf2.png", layout="centered")
st.header("Carbon Capture Buddy!")

# Text input for questions
input_text = st.text_input("Ask a question (e.g., 'What is the carbon footprint of a plastic bottle?'):", key="input")

# Image upload functionality
uploaded_file = st.file_uploader("Optionally, upload an image related to your question...", type=["jpg", "jpeg", "png"])
image = None
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Submit button
submit = st.button("Get Answer")

# Display the response if submit button is clicked
if submit:
    response = get_gemini_response(input_text, image)
    st.subheader("Response:")
    st.write(response)
