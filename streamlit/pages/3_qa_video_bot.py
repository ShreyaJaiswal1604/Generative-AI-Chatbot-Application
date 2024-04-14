import streamlit as st
import os

from pinecone import Pinecone, PodSpec
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from utils import *
import base64
# from dotenv import load_dotenv
# load_dotenv()

# Set background image
def sidebar_bg(side_bg):

   side_bg_ext = 'jpeg'

   st.markdown(
      f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
          background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
      }}
      </style>
      """,
      unsafe_allow_html=True,
      )
   
side_bg_ext = '../images/04-img.jpeg'

sidebar_bg(side_bg_ext)



# if 'messages' not in st.session_state:
st.session_state.messages = None

st.header(":tv: YouTube Chat Bot",divider="rainbow")

st.subheader('Hi There, Go ahead and ask your query!', divider='orange')

pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENVIRONMENT", "gcp-starter"),
)
embeddings = OpenAIEmbeddings(api_key=os.getenv('OPENAI_API_KEY'))
pinecone = PineconeVectorStore.from_existing_index(
    os.getenv("PINECONE_INDEX_NAME", "sandbox-yt"), embeddings
)


template = """
            Answer the question based on the context below. If you can't
            answer the question, reply "I don't know".
            Context: {context}
            Question: {question}
          """

prompt = ChatPromptTemplate.from_template(template)
parser = StrOutputParser()
model = ChatOpenAI(model="gpt-3.5-turbo")

chain = (
    {"context": pinecone.as_retriever(), "question": RunnablePassthrough()}
    | prompt
    | model
    | parser
)

reset_button = st.button("Reset Chat", key="reset_button")
if reset_button:
    st.session_state.messages = None

if st.session_state.messages is None:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "Based on the pre-processed videos, you can ask me anything about them",
        }
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    msg = chain.invoke(st.session_state.messages[-1]["content"])
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
