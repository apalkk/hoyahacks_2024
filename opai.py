from langchain.chat_models import ChatOpenAI
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from langchain.chains import VectorDBQA
from langchain.document_loaders.unstructured import UnstructuredFileLoader
import pymongo

# client = pymongo.MongoClient(
#    "mongodb+srv://aadipalnitkar96:m6DCib70qyEk1r8I@hoya.32uxq9h.mongodb.net/?retryWrites=true&w=majority")
# db = client.myDatabase

        vector_search = MongoDBAtlasVectorSearch.from_connection_string(
                MONGODB_ATLAS_CLUSTER_URI,
                "myDatabase.recipes",
                OpenAIEmbeddings(disallowed_special=()),
                index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
                )

qa = VectorDBQA.from_chain_type(
    llm=ChatOpenAI(), chain_type="stuff", vectorstore=db, k=1)

query = "What is the document about"
qa.run(query)

