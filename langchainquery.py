from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
import os
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI


MONGODB_ATLAS_CLUSTER_URI = "mongodb+srv://kennywu:helloworld@cluster1.9ot8jux.mongodb.net/?retryWrites=true&w=majority"

DB_NAME = "myDatabase"
COLLECTION_NAME = "VectorStorage"
ATLAS_VECTOR_SEARCH_INDEX_NAME = "vectorSearch"

vector_search = MongoDBAtlasVectorSearch.from_connection_string(
    MONGODB_ATLAS_CLUSTER_URI,
    DB_NAME + "." + COLLECTION_NAME,
    OpenAIEmbeddings(disallowed_special=()),
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
)

qa_retriever = vector_search.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 10},
)

PROMPT_TEMPLATE = """
Output text that answers the desired question based on a context you are given.

Imagine you are helping me interact with high-school students to help them understand the University of Maryland better. Act as if you were a college advisor.

You are only allowed to use the information given to you in the context to answer the question concisely.

Remember, you will be first given a context then the question you must answer the question provided next.

Context:
{context}

Question: 
{question}
"""

PROMPT = PromptTemplate(
    template=PROMPT_TEMPLATE, input_variables=["context", "question"]
)


def query_q(question: str):
    QA = RetrievalQA.from_chain_type(
        llm=OpenAI(),
        chain_type="stuff",
        retriever=qa_retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT},
    )

    docs = QA({"query": question})
    return docs["result"]
