import getpass
import os
from pymongo import MongoClient
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings

MONGODB_ATLAS_CLUSTER_URI = "mongodb+srv://kennywu:helloworld@cluster1.9ot8jux.mongodb.net/?retryWrites=true&w=majority"

# initialize MongoDB python client
client = MongoClient(MONGODB_ATLAS_CLUSTER_URI)

DB_NAME = "myDatabase"
COLLECTION_NAME = "VectorStorage"
ATLAS_VECTOR_SEARCH_INDEX_NAME = "vectorSearch"
MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]
FOLDER_PATH = "admissions/"

for filename in os.listdir(FOLDER_PATH):
    loader = TextLoader(os.path.join(FOLDER_PATH, filename))
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = text_splitter.split_documents(data)
    vector_search = MongoDBAtlasVectorSearch.from_documents(
        documents=docs,
        embedding=OpenAIEmbeddings(disallowed_special=()),
        collection=MONGODB_COLLECTION,
        index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    )
