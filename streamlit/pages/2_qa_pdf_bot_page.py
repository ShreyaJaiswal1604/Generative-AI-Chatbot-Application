
import streamlit as st
import os
from utils import *
# from dotenv import load_dotenv
# load_dotenv()
# if st.session_state.messages is None:
#     st.session_state.messages = None

st.session_state.messages = None

st.header(":page_with_curl:Your PDF Bot - PDFPilot")

st.subheader('Hi There, Go ahead and ask your query!', divider='rainbow')

pc = Pinecone(api_key=os.environ.get('PINECONE_API_KEY'))
index_name =  os.environ.get('PINECONE_INDEX_NAME','pdf-qa-chatbot-streamlit')
index = get_or_create_index(pc=pc,index_name=index_name)
embed_model = "text-embedding-ada-002"

# query = st.text_input("Ask a question:", "")

# if st.button("Retrieve and Answer"):
#     query_with_contexts = retrieve(query=query,index=index,embed_model=embed_model)
#     with st.spinner("Going through your document......."):
#         answer=complete(query_with_contexts)
#         st.write("Answer:", answer)



# st.divider()

reset_button = st.button("Reset Chat", key="reset_button")

if reset_button:
    st.session_state.messages = None

if st.session_state.messages is None:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "Based on the pre-processed files, you can ask me anything about them",
        }
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    query_with_contexts = retrieve(query=prompt,index=index,embed_model=embed_model)
    msg = complete(query_with_contexts)
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)