import streamlit as st
from dotenv import load_dotenv
from PIL import Image
import os
import json
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to save chat history to a file
def save_chat_history(history, filename="chat_history.json"):
    with open(filename, "w") as f:
        json.dump(history, f)

# Function to load chat history from a file
def load_chat_history(filename="chat_history.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Initialize chat history by loading it from file at the start of the session
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = load_chat_history()

# Initialize the current page
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'  # Set initial page to home

# Function to load the model and get responses
def get_gemini_response(input_text, image=None):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Check if the question is about carbon footprint
    if "carbon footprint" in input_text.lower():
        input_text = f"Provide a rough average value for the carbon footprint for the following object or activity: {input_text}, if the item is not environment friendly, suggest an alternative in a few lines. Suggest brands of the item with low carbon footprint."

    # Generate the response based on input and image
    if input_text:
        response = model.generate_content([input_text, image] if image else [input_text])
    else:
        response = model.generate_content(image)
    
    return response.text

# Initialize Streamlit app with green gradient theme
st.set_page_config(page_title="Carbon Footprint Demo", page_icon="🌱", layout="centered")

# Custom CSS for gradient background, spacing, and styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(green, white);  /* Gradient from light green to white */
        padding: 20px;  /* Adding padding around the app */
    }
    h1, h2, h3, h4, h5, h6, p, div, label, .stButton > button {
        color: green;
    }
    .stButton > button {
        background-color: #e8f5e9;
        color: green;
        border: none;
        border-radius: 10px;  /* Adding border radius for buttons */
        padding: 10px 20px;  /* Adding padding for buttons */
        margin: 10px 0;  /* Spacing between buttons */
        font-size: 16px;  /* Larger font for buttons */
    }
    .stTextInput > div > div > input, .stFileUploader > div {
        background-color: #f1f8e9;
        color: green;
        border: 2px solid #8b4513; /* Brown border */
        border-radius: 10px;
        padding: 10px;  /* Adding padding to input fields */
    }
    .stFileUploader div[role="button"] {
        background-color: #4CAF50; /* Green background */
        color: white; /* White text for contrast */
        border-radius: 10px;
        padding: 10px;  /* Padding for the file uploader */
    }
    .stTextInput > div > div > input:focus, .stFileUploader > div:focus {
        outline: none; /* Remove black border on focus */
    }
    /* Style for chat history and expander */
    .stExpander { 
        margin-top: 10px;  /* Space above the expander */
        background-color: #f9f9f9;  /* Light background for expanders */
        padding: 10px;  /* Padding inside expanders */
        border: 1px solid #d0d0d0;  /* Light gray border */
        border-radius: 10px;  /* Rounded corners for expanders */
    }
    </style>
""", unsafe_allow_html=True)

# Navigation Button to enter the chatbot
if st.button("Enter E-ChatBot"):
    st.session_state.current_page = 'chatbot'

# Display content based on the current page
if st.session_state.current_page == 'home':
    st.header("🌱 Welcome to Carbon Capture Buddy!")
    st.write("Your assistant for understanding carbon footprints and eco-friendly alternatives.")
    st.write("Feel free to explore our chatbot to ask questions about carbon footprints.")

elif st.session_state.current_page == 'chatbot':
    st.header("🌱 Carbon Capture Buddy - E-ChatBot")

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
    if submit and input_text:
        response = get_gemini_response(input_text, image)
        st.session_state.chat_history.append((input_text, response))  # Store in session state
        save_chat_history(st.session_state.chat_history)  # Save to file
        st.subheader("Response:")
        st.write(response)

    # Section to display chat history with collapsible answers
    st.subheader("Chat History")
    for i, (question, answer) in enumerate(st.session_state.chat_history):
        with st.expander(f"Question {i + 1}: {question}"):
            st.write(answer)

    # Option to clear chat history
    if st.button("Clear Chat History"):
        st.session_state.chat_history.clear()
        save_chat_history([])  # Clear the file as well
        st.success("Chat history cleared!")

    # Go back home button should only be shown on the chatbot page
    if st.button("Go to Home"):
        st.session_state.current_page = 'home'
