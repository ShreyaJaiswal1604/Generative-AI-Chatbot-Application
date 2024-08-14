<hr>

# 🌟 Generative AI Chatbot Application 🌟
<hr>

## Project Details 📝

The Generative AI Chatbot Application is designed to simplify interactions with YouTube links and PDF files. It leverages advanced technologies to provide engaging and efficient responses to user queries about the content within these media sources.

**Key Features:**
- **PDF Processing**: Upload and interact with PDF documents to extract and query content.
- **YouTube Integration**: Access pre-processed video content and interact with it via chatbot functionality.
- **Generative AI**: Utilize cutting-edge AI models to provide accurate and contextually relevant responses.

![til](https://github.com/ShreyaJaiswal1604/Generative-AI-Chatbot-Application/blob/main/videos/chatbot-demo.gif)

---
## Tools and Technologies 🛠️

### 🔧 Core Technologies:
- **Python**: The backbone of the application, providing robustness and flexibility.
- **Streamlit**: Empowers the creation of intuitive and interactive user interfaces.
- **Pinecone Vector DB**: Efficiently handles vector storage for seamless data retrieval.
- **OpenAI Embeddings**: Enhances the chatbot's understanding and response capabilities.
- **LangChain**: Facilitates chaining of language model components for complex queries.

### 📦 Libraries and Frameworks:
- **pdfplumber**: For extracting text from PDF files.
- **langchain_openai**: To interact with OpenAI's embeddings and chat models.
- **langchain_pinecone**: Integrates Pinecone vector store with LangChain.
- **base64**: For encoding images and data.

## Project Architecture 🏗️

![Generative AI Chatbot Architecture](https://github.com/ShreyaJaiswal1604/Generative-AI-Chatbot-Application/blob/main/images/architecture/genai-chatbot-application.png)

### 1. **Frontend**:
- **Streamlit**: Powers the interactive user interface, allowing users to upload PDFs, input YouTube links, and interact with the chatbot.

### 2. **Backend**:
- **PDF Processing**: Utilizes `pdfplumber` for text extraction and cleaning, converting PDF content into a format suitable for querying.
- **Vector Storage**: Uses Pinecone to store and retrieve vector embeddings of the document and video content.
- **AI Integration**: OpenAI's embeddings and chat models generate and refine responses based on user queries and retrieved context.

### 3. **Data Flow**:
- **PDF Upload**: Users upload PDFs, which are then processed to extract and clean text. This text is split into chunks and embedded into Pinecone.
- **YouTube Integration**: Users can interact with pre-processed video content. For future enhancements, video processing will be added.
- **Query Handling**: User queries are processed by creating embeddings using OpenAI, retrieved from Pinecone, and answered by a generative AI model.

## Project Application 🚀

### **1. PDF Interaction**:
- Users upload PDF files, which are processed and indexed.
- Users can query the content of the PDFs, and the chatbot provides answers based on the indexed data.

### **2. YouTube Integration**:
- Users can interact with pre-processed video content.
- Users can input queries related to the video content, and the chatbot provides responses based on pre-processed information.

### **3. User Interaction**:
- A chat interface allows users to ask questions about the content in a conversational manner.
- Users receive responses from the chatbot based on the context retrieved from Pinecone and processed by OpenAI's language models.

## Main Features 🌟

1. **PDF Upload and Interaction 📄**
   - **PDF Processing**: Upload PDF documents directly and extract text.
   - **Text Extraction**: Automatically cleans and processes text from the uploaded PDFs.
   - **Contextual Queries**: Query PDF content with responses based on indexed text.

2. **YouTube Integration 📹**
   - **Video Access**: Interact with pre-processed YouTube videos.
   - **Video Content Queries**: Ask questions about video content, with answers derived from pre-processed information.

3. **Generative AI Responses 🤖**
   - **Contextual Understanding**: Utilizes OpenAI embeddings to understand and process user queries.
   - **Advanced Response Generation**: Produces accurate and contextually relevant answers using OpenAI’s language models.

4. **Interactive Chat Interface 💬**
   - **User-Friendly Interface**: Streamlit provides an intuitive chat interface.
   - **Chat History**: Maintains session-based chat history for ongoing conversations.

5. **Efficient Vector Storage and Retrieval 🗃️**
   - **Pinecone Integration**: Manages and retrieves vector embeddings of PDF and video content efficiently.
   - **Fast Query Handling**: Quick access to relevant content through vector similarity search.

6. **Customizable Backgrounds and UI 🎨**
   - **Dynamic Backgrounds**: Customizable sidebar backgrounds and images for a personalized touch.
   - **Interactive Elements**: Engaging UI elements and decorations to enhance the user experience.

## Installation and Setup 🛠️

To run this application locally, follow these steps:

Follow these steps to run the application locally:

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>

2. Install the necessary dependencies:

```bash
   pip install -r requirements.txt
```

3. Configure your environment variables:

`PINECONE_API_KEY`: <Your Pinecone API key>
`OPENAI_API_KEY:`: <Your OpenAI API key>

4. Launch the Streamlit application:

```bash
   streamlit run main.py
```

Enjoy exploring the world of YouTube videos and PDF documents with our Chatbot Application!
