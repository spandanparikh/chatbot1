import streamlit as st
import PyPDF2

def read_pdf_text(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text() + '\n'
    return text

#Upload the PDF files
st.header("My First Chatbot")

with st.sidebar:
    st.title("Your documents")
    file = st.file_uploader("Upload a PDF file", type="pdf")
    
#Extract the text
if file is not None:
    pdf_text = read_pdf_text(file.name)
    # st.write(pdf_text)

#Break it into chaunks

