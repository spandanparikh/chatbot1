import streamlit as st
import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.chat_models import ChatOpenAI
# from langchain_community.llms import HuggingFaceHub


#HUGGING_FACE_API_KEY = "<Key>" #Huggingface-KEY
OPENAI_API_KEY = "<openaikey>"

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

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n"],
        chunk_size=1000,
        chunk_overlap = 150,
        length_function = len
    )
    
    chunks = text_splitter.split_text(pdf_text)
    #st.write(chunks)
    
    #generaring embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    #creating vector store - FAISS
    vector_store = FAISS.from_texts(chunks, embeddings)
    #Above statment does 3 things.
    #1. It creates embeddings using openAI
    #2. initiazes the FAISS
    #3. store chunks & embeddings
    
    
    #get user questions
    user_questions = st.text_input("Type your questions here")
    
    #do similarity search
    
    if user_questions:
        match = vector_store.similarity_search(user_questions)
        #st.write(match)
        
        #define the LLM
        llm = ChatOpenAI(
            openai_api_key = OPENAI_API_KEY,
            temperature = 0,
            max_tokens = 1000,
            model_name = "gpt-3.5-turbo"
        )
        
        
        '''
        # Requires you to set HUGGINGFACEHUB_API_TOKEN as env variable
        llm = HuggingFaceHub(
            repo_id="google/flan-t5-large",   # pick any open LLM
            model_kwargs={"temperature":0.7, "max_length":512},
            huggingfacehub_api_token = HUGGING_FACE_API_KEY,
            task="text2text-generation" 
        )
        '''
        
        #chain -> take the question , get relavant document, pass it to the LLM, generate the output
        chain = load_qa_chain(llm, chain_type="stuff")
        response = chain.run(input_documents = match, question = user_questions)
        
        #Print the output
        st.write(response)
         