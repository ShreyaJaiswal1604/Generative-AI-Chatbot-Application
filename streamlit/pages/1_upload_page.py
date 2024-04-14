import streamlit as st
import os
from utils import *
from pinecone import Pinecone, PodSpec
from openai import OpenAI
import base64


pin_api_key=os.environ.get('PINECONE_API_KEY')
openai_api_key=os.getenv('OPENAI_API_KEY')


pc = Pinecone(api_key=os.environ.get('PINECONE_API_KEY'))
#pc.list_indexes().names()
cloud = os.environ.get('PINECONE_CLOUD','aws') 
region = os.environ.get('PINECONE_REGION','us-east-1') 
spec = ServerlessSpec(cloud=cloud, region=region)
index_name =  os.environ.get('PINECONE_INDEX_NAME','pdf-qa-chatbot-streamlit')
embed_model = "text-embedding-ada-002"

# Set background image
def sidebar_bg(side_bg):

   side_bg_ext = 'png'

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
   
side_bg_ext = '../images/02-img.png'

sidebar_bg(side_bg_ext)

# openai.api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI()

def upsert_embeddings(pc, index_name, preprocessed_data, embed_model):
    index = pc.Index(index_name)

    for document in preprocessed_data:
        res = client.embeddings.create(
            input=[document.page_content],
            # input=[document.page_content],
            model=embed_model
            # engine=embed_model
        )
        # embeddings = res['data'][0]['embedding']
        # index.upsert(vectors=[{"id": document.metadata['unique_id'], "values": embeddings, "metadata": document.metadata}])

        # Assuming there's a method to get the embeddings directly
        # embeddings = res.get_embedding()  # Adjust this according to the actual method or attribute
        embeddings = res.data[0].embedding
        index.upsert(vectors=[{"id": document.metadata['unique_id'], "values": embeddings, "metadata": document.metadata}])



st.header("Welcome to your Document Source Station!",divider='rainbow')
options = st.selectbox("Select the type of data got the bot to read",
                        options=['Waiting for your input','Video URL','PDF'])


#ask a query based on options of data sources
if options == 'PDF':
    st.subheader("PDF Document Upload", divider="blue")

    uploadedpdf = st.file_uploader("Upload a PDF", type=["pdf"])


    if uploadedpdf:
        document = convert_str_to_doc(uploadedpdf)
        progress_bar = st.progress(0)
        st.success("PDF Document uploaded successfully!")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
        preprocessedata = text_splitter.split_documents(document)
        #create_or_connect_index(pc=pc, index_name=index_name, spec=spec)\
        # check if index already exists (it shouldn't if this is first time)
        # print(f"Index List {pc.list_indexes().names()}")
        index = get_or_create_index(pc=pc,index_name=index_name)
        # time.sleep(5)
        index.describe_index_stats()
        with st.spinner("Database Initializing......"):
            upsert_embeddings(pc=pc, index_name=index_name,preprocessed_data=preprocessedata,embed_model=embed_model)
            st.success("Database Uploaded successfully!")
            time.sleep(2)
            st.switch_page("pages/2_qa_pdf_bot_page.py")

    st.divider()

if options == 'Video URL':
    #st.subheader(":tv: YouTube Chat Bot", divider="red")
    st.header(":tv: YouTube Chat Bot",divider="red")
    st.header("Pre Processed Videos")
    video_db = [
        {
            "title": "Tech Expert Warns of AI's Potentially Dangerous Capabilities",
            "url": "https://youtube.com/watch?v=chfj7RHA5vM",
            "thumbnail": "https://i.ytimg.com/vi/chfj7RHA5vM/sddefault.jpg",
        },
        {
            "title": "You Have to Make Happiness Your Priority - Naval Rakivant",
            "url": "https://youtube.com/watch?v=Z4Q9P_EhiY0",
            "thumbnail": "https://i.ytimg.com/vi/Z4Q9P_EhiY0/sddefault.jpg",
        },
    ]

    for videos in video_db:
        with st.expander(videos["title"]):
         st.video(videos["url"])

    st.divider()

    st.header("Bespoke Video Processing")
    with st.form("video_form"):
        video_url = st.text_input("Enter a YouTube URL")

        submitted = st.form_submit_button("Coming Soon", disabled=True)
        if submitted:
            pass

    if(st.button("Let's see what our Video Bot can answer with the preprocessed video..!!")):
        st.switch_page("pages/3_qa_video_bot.py")



# if button:
#     st.switch_page("pages/2_qa_page.py")
