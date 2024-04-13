#import PyPDF2
import pdfplumber
import os
import uuid
import datetime
import re
import time
from langchain_core.documents.base import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone
from pinecone import ServerlessSpec
from pinecone import PodSpec
from openai import OpenAI

client = OpenAI()

def clean_text(text):
    # Remove newline characters
    cleaned_text = text.replace('\n', '')
    # Remove non-alphanumeric characters
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', cleaned_text)
    # Replace multiple whitespace characters with a single space
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    # Strip leading and trailing whitespace
    cleaned_text = cleaned_text.strip()
    return cleaned_text

def convert_str_to_doc(uploadedpdf):
    data = []
    documents = []
    with pdfplumber.open(uploadedpdf) as pdf:
        pages = pdf.pages
        for i, page in enumerate(pages):
            data.append(page.extract_text())
            unique_id = str(uuid.uuid4())
            filename = os.path.splitext(uploadedpdf.name)[0]
            upload_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            page_number = i+1
            cleaned_data_content = clean_text(page.extract_text())
            metadata = {"unique_id": unique_id, "filename": filename, "upload_date":upload_date, "page_number":page_number, "text":cleaned_data_content}
            documents.append(Document(page.extract_text(),metadata = metadata))
    #strdata = ' '.join(data)  
    return documents


def create_or_connect_index(pc, index_name, spec):
    # Check if index exists
    if index_name not in pc.list_indexes().names():
        # Create index if it doesn't exist
        pc.create_index(
            index_name,
            dimension=1536,  # dimensionality of text-embedding-ada-002
            metric='cosine',
            spec=spec
        )
    
    # Connect to the index
    index = pc.Index(index_name)
    
    # View index stats
    index.describe_index_stats()


# def upsert_embeddings(pc, index_name, preprocessed_data, embed_model):
#     index = pc.Index(index_name)

#     for document in preprocessed_data:
#         res = openai.Embedding.create(
#             input=[document.page_content],
#             engine=embed_model
#         )
#         embeddings = res['data'][0]['embedding']
#         index.upsert(vectors=[{"id": document.metadata['unique_id'], "values": embeddings, "metadata": document.metadata}])


def retrieve(query, index, embed_model):
    # Create embeddings for the query
    res = client.embeddings.create(
            input=[query],
            # input=[document.page_content],
            model=embed_model
            # engine=embed_model
        )
    
    # res = openai.Embedding.create(input=[query], engine=embed_model)
    xq = res.data[0].embedding
    # xq = res['data'][0]['embedding']

    # Retrieve relevant contexts from Pinecone
    contexts = []
    time_waited = 0
    while len(contexts) < 3 and time_waited < 60 * 12:
        res = index.query(vector=xq, top_k=10, include_metadata=True)
        # Extract text from metadata for each match
        contexts += [x['metadata']['text'] for x in res['matches'] if 'metadata' in x and 'text' in x['metadata']]
        print(f"Retrieved {len(contexts)} contexts, sleeping for 15 seconds...")
        # time.sleep(5)
        # time_waited += 15

    if time_waited >= 60 * 12:
        print("Timed out waiting for contexts to be retrieved.")
        contexts = ["No contexts retrieved. Try to answer the question yourself!"]

    # Build prompt with retrieved contexts
    prompt_start = "Answer the question based on the context below.\n\nContext:\n"
    prompt_end = f"\n\nQuestion: {query}\nAnswer:"

    # Combine contexts until reaching the limit
    prompt_contexts = "\n\n---\n\n".join(contexts)
    if len(prompt_contexts) > 500:
        prompt = prompt_start + "\n\n---\n\n".join(contexts[:2]) + prompt_end
    else:
        prompt = prompt_start + prompt_contexts + prompt_end

    return prompt


def complete(prompt):
    # instructions
    sys_prompt = "You are a helpful assistant that always answers questions."
    # query text-davinci-003
    res = client.chat.completions.create(
        model='gpt-3.5-turbo-0613',
        # response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return res.choices[0].message.content
    # return res['choices'][0]['message']['content'].strip()




def get_or_create_index(pc, index_name):
    if index_name not in pc.list_indexes().names():
        # If index does not exist, create it
        pc.create_index(
            index_name,
            dimension=1536,
            metric='cosine',
            spec=PodSpec(environment="gcp-starter")
        )
    # Connect to index
    index = pc.Index(index_name)
    return index
