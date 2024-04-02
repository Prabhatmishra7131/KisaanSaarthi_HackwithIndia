import google.generativeai as genai
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Configure the GenerativeAI API key using the loaded environment variable
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up the model configuration for text generation
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

# Define safety settings for content generation
safety_settings = [
    {"category": f"HARM_CATEGORY_{category}", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
    for category in ["HARASSMENT", "HATE_SPEECH", "SEXUALLY_EXPLICIT", "DANGEROUS_CONTENT"]
]

# Initialize the GenerativeModel with the specified model name, configuration, and safety settings
model = genai.GenerativeModel(
    model_name="gemini-pro-vision",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

# Function to read image data from a file object
def read_image_data(file):
    if file is None:
        raise ValueError("No file provided.")
    return {"mime_type": file.type, "data": file.read()}

# Function to generate a response based on a prompt and an image data
def generate_gemini_response(prompt, image_data):
    response = model.generate_content([prompt, image_data])
    return response.text

# Function to process uploaded files and generate a response
def process_uploaded_files(file):
    if file is not None:
        response = generate_gemini_response(input_prompt, read_image_data(file))

        st.subheader("### **Analysis:**")

        # Display the response in a Markdown-styled text box
        st.markdown(response, unsafe_allow_html=True)
    else:
        st.write("Please upload an image for analysis.")

# Initial input prompt for the plant pathologist
input_prompt = """
As a highly skilled plant pathologist, your expertise is indispensable in our pursuit of maintaining optimal plant health. You will be provided with information or samples related to plant diseases, and your role involves conducting a detailed analysis to identify the specific issues, propose solutions, and offer recommendations.

**Analysis Guidelines:**

1. **Disease Identification:** Examine the provided information or samples to identify and characterize plant diseases accurately.

2. **Detailed Findings:** Provide in-depth findings on the nature and extent of the identified plant diseases, including affected plant parts, symptoms, and potential causes.

3. **Next Steps:** Outline the recommended course of action for managing and controlling the identified plant diseases. This may involve treatment options, preventive measures, or further investigations.

4. **Recommendations:** Offer informed recommendations for maintaining plant health, preventing disease spread, and optimizing overall plant well-being.

5. **Important Note:** As a plant pathologist, your insights are vital for informed decision-making in agriculture and plant management. Your response should be thorough, concise, and focused on plant health.

**Disclaimer:**
*"Please note that the information provided is based on plant pathology analysis and should not replace professional agricultural advice. Consult with qualified agricultural experts before implementing any strategies or treatments."*

Your role is pivotal in ensuring the health and productivity of plants. Proceed to analyze the provided information or samples, adhering to the structured 
"""

# Streamlit app setup
st.set_page_config(page_title="Plant Pathologist", page_icon=":seedling:", layout="wide")

st.title("Plant Pathologist")

uploaded_file = st.file_uploader("Click to Upload an Image", type=["jpg", "jpeg", "png", "gif", "bmp", "webp"], key="file_uploader")

if uploaded_file:
    process_uploaded_files(uploaded_file)
