from haystack import Pipeline
from haystack.document_stores.mongodb_atlas import MongoDBAtlasDocumentStore
from haystack.nodes import TextConverter, PreProcessor

document_store = MongoDBAtlasDocumentStore(
    mongo_connection_string="mongodb+srv://aadipalnitkar96:m6DCib70qyEk1r8I@hoya.32uxq9h.mongodb.net/?retryWrites=true&w=majority",
    database_name="myDatabase",
    collection_name="recipes",
    vector_search_index="vector_search_index",
    embedding_dim=1536,
)
converter = TextConverter()
preprocessor = PreProcessor()

indexing_pipeline = Pipeline()
indexing_pipeline.add_node(component=converter, name="TextConverter", inputs=["File"])
indexing_pipeline.add_node(
     component=preprocessor, name="PreProcessor", inputs=["TextConverter"]
)
indexing_pipeline.add_node(
     component=document_store, name="DocumentStore", inputs=["PreProcessor"]
)

indexing_pipeline.run(
     file_paths=["applications_deadlines.txt", "freshman_applicants_file.txt"]
)
