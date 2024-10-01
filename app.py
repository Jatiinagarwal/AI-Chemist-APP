### Health Management App
from dotenv import load_dotenv

load_dotenv()  ## load all the environment variables
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load google gemini pro vision API and get response

def get_gemini_response(input,image,prompt):
    model=genai.GenerativeModel("gemini-1.5-flash")
    response=model.generate_content([input,image[0],prompt])
    return response.text


def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read thje file into bytes
        bytes_data=uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type":uploaded_file.type, # get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
## initialize our streamlit app


input_prompt="""
You are an expert pharmacetical/Chemist ehere you need to see the tablets from the image and ,
also provide the details of every drug/tablets items with below format

    1. Examine the image carefully and identify the tablets depicted.
    2. Describe the uses and functionalities of each tablet shown in the image.
    3. Provide information on the intended purposes, features, and typical applications of the tablets.
    4. If possible, include any notable specification or distinguishing characteristics of each tablet.
    5. Ensure clarity and conciseness in your description, focusing on key details and distinguishing features.
    ....
"""

## initialize our streamlit app

st.set_page_config(page_title="AI Chemist APP")
st.header("AI Chemist APP")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file=st.file_uploader("Choose an image...", type=['jpg','jpeg','png'])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit=st.button("Tell me")

## if submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)