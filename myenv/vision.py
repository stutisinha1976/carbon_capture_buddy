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
        background: linear-gradient(#F6FCDF,#859F3D);  /* Gradient from white to green */
        padding: 20px;  /* Adding padding around the app */
       
    }
    h1, h3, h4, h5, h6,label,p {
       
        font-size: 18px;  /* Larger font for headers */
        color: #16423C;
    }
    h2{
        font-size: 40px;
        color: #16423C;
        font-weight: bold;
        font-family: roboto;
        
    }
    .stButton > button {
        background-color: transparent !important; /* Green background for buttons */
         /* Black text for contrast */
         border: 2px solid #16423C; /* Green border for buttons */
        color: white !important; /* White text for contrast */;
        border-radius: 20px !important; /* Rounded corners */
        
        font-size: 16px !important; /* Increase font size for buttons */
        margin: 10px 5px 10px!important; /* Add spacing around buttons */
    }
    .stButton > button:hover {
        background-color: green; /* Lighter green on hover */;
        border:1px solid green;/* Darker green on hover */
        shadow: 20px 2px 2px grey;
    }
    .stTextInput > div > div > input, .stFileUploader > div {
        background-color: #f1f8e9;
        color: #ACF60B;
        border: 2px solid #8b4513; /* Brown border */
        border-radius: 10px;
        padding: 10px;  /* Adding padding to input fields */
    }
    .stFileUploader div[role="button"] {
        background-color: white !important; /* White background */
        color: black !important; /* Black text for contrast */
        border: 2px solid #000000 !important; /* Black border */
        border-radius: 10px; /* Rounded corners */
        padding: 10px !important; /* Padding for the file uploader */
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


# Display content based on the current page
if st.session_state.current_page == 'home':
    
    st.header("🌱 Welcome to Carbon Capture Buddy!")
    st.write("Your assistant for understanding carbon footprints and eco-friendly alternatives.")
    st.write("Feel free to explore our chatbot to ask questions about carbon footprints.")
    if st.button("Enter ChatBot"):
        st.session_state.current_page = 'chatbot'

elif st.session_state.current_page == 'chatbot':
    st.header("🌱 Carbon Capture Buddy - ChatBot")

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

    # Card with a link to the SDGs page
    st.markdown("""
        <div style="background-image:url('https://www.google.com/url?sa=i&url=https%3A%2F%2Fcid-inc.com%2Fblog%2Fleaf-area-how-why-measuring-leaf-area-is-vital-to-plant-research%2F&psig=AOvVaw0kFgfU-UY222zpn88uc210&ust=1732202977395000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCMCV1Iqd64kDFQAAAAAdAAAAABAG'); padding: 10px; border-radius: 10px; border: 2px solid #31511E; margin-top: 20px;">
            <h3 style="text-align: center; color: #31511E; margin-bottom: 10px;">Learn More About the 17 Sustainable Development Goals</h3>
            <p style="text-align: center; color: #31511E;">Discover how the SDGs contribute to a better future for all.</p>
            <div style="text-align: center;">
                <a href="https://sdgs.un.org/goals" target="_blank" style="text-decoration: none; background-color: green; color: white; padding: 10px 20px; border-radius: 5px; font-size: 16px;">Explore the SDGs</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Go back home button should only be shown on the chatbot page
    if st.button("Go to Home"):
        st.session_state.current_page = 'home'
