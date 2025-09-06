Cource Link: https://ibm-learning.udemy.com/course/generative-ai-for-beginners-b/learn/lecture/40913810#overview


1. Install the required packages which are mentioned in install-required-packages.txt file.

2. I have used wsl in windows

3. Run command manually in wsl : 
source ~/.venvs/streamlit-env/bin/activate

4. Run the script file run.sh

5. copy past the url into chrome browser for further work



Note, I got error of :
openai.RateLimitError: Error code: 429 - {'error': {'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.', 'type': 'insufficient_quota', 'param': None, 'code': 'insufficient_quota'}}

so I am moving to another approach of Switch to a local embedding model (no API quota needed)

For example, use HuggingFace sentence-transformers  instead of OpenAI embeddings:

from langchain_community.embeddings import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_store = FAISS.from_texts(chunks, embeddings)
