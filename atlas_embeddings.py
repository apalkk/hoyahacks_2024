import sys
import requests
import pymongo

client = pymongo.MongoClient(
    "mongodb+srv://aadipalnitkar96:m6DCib70qyEk1r8I@hoya.32uxq9h.mongodb.net/?retryWrites=true&w=majority")
db = client.myDatabase
collection = db["recipes"]

recipe_documents = [{"contents": open("requirements.txt", "r").read()}]

try:
    collection.drop()

# return a friendly error if an authentication error is thrown
except pymongo.errors.OperationFailure:
    print("An authentication error was received. Are your username and password correct in your connection string?")
    sys.exit(1)

# INSERT DOCUMENTS
#
# You can insert individual documents using collection.insert_one().
# In this example, we're going to create four documents and then
# insert them all with insert_many().

try:
    result = collection.insert_many(recipe_documents)

# return a friendly error if the operation fails
except pymongo.errors.OperationFailure:
    print("An authentication error was received. Are you sure your database user is authorized to perform write operations?")
    sys.exit(1)



hf_token = "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"
embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"


def generate_embedding(text: str) -> list[float]:
    response = requests.post(
        embedding_url,
        headers={"Authorization": f"Bearer {hf_token}"},
        json={"inputs": text})
    if response.status_code != 200:
        raise ValueError(
            f"Request failed with status code {response.status_code}: {response.text}")
    return response.json()


for doc in collection.find({'contents': {"$exists": True}}).limit(50):
    doc['plot_embedding_hf'] = generate_embedding(doc['contents'])
    collection.replace_one({'_id': doc['_id']}, doc)
