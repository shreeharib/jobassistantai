import base64
import streamlit as st
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai

genai.configure(api_key="AIzaSyDsTc0o5asIFFJ4wunmJS0b3qb6RXSMg0")

def get_gemini_response(input,pdf_cotent,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,pdf_cotent[0],prompt])
    return response.text

def get_gemini_project(input,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([input,prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App

st.set_page_config(page_title="ATS Resume EXpert")
st.header("Job Assistant AI : Get placed in your dream Job")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")


submit1 = st.button("Tell Me About the Resume")

#submit2 = st.button("How Can I Improvise my Skills")

submit3 = st.button("Percentage match")
submit4 = st.button("Get Relevant Projects")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""
input_prompt4 = """
I want you to respond only in English (US). Act in the role of specialist in analysing job descriptions and generating projects that companies will like. The writing style is to-the-point and straightforward, with easy-to-read sentences aimed at persons aged 18. It is important that the language is not too difficult. It would be nice if the text can be written at B1 level. I want you to provide me the project recommendations which aligns with companies interests and job descriptions also with technology which I should use for the projects in order to maximize my chances of getting shortlisted with the project, make it in table which should contain the project, description about the project, technology to be used and basic brief about how we can get it done? and also make a column as ranking by giving % of chances of getting shortlisted with that project. - The Job description is as attached.

"""
if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")
elif submit4:
    if uploaded_file is not None:
        response=get_gemini_project(input_prompt4,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")



   




