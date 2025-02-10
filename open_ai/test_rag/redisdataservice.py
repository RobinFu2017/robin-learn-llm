import numpy as np
from openai import OpenAI
from pdfservice import pdf_to_embeddings

client = OpenAI()

from redis.commands.search.field import TextField, VectorField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query

import redis

INDEX_NAME = "embeddings-index"           # name of the search index
PREFIX = "doc"                            # prefix for the document keys
# distance metric for the vectors (ex. COSINE, IP, L2)
DISTANCE_METRIC = "COSINE"

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PASSWORD = "" 

class RedisDataService():

    def __init__(self):
        # Connect to Redis
        self.redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD
        )

    def drop_data(self, index_name: str = INDEX_NAME):
        print('start to drop_redis_data')
        try:
            self.redis_client.ft(index_name).dropindex()
            print('Index dropped')
        except:
            # Index doees not exist
            print('Index does not exist')

    def load_data_from_pdf(self, pdf : str):
        embeddings = pdf_to_embeddings(pdf_path = pdf)
        print('start to load date to redis')
        # Constants
        vector_dim = len(embeddings[0]['vector'])  # length of the vectors
        
		# Initial number of vectors
        vector_number = len(embeddings)

        # Define RediSearch fields
        text = TextField(name="text")
        text_embedding = VectorField("vector",
                                     "FLAT", {
                                         "TYPE": "FLOAT32",
                                         "DIM": vector_dim,
                                         "DISTANCE_METRIC": DISTANCE_METRIC,
                                         "INITIAL_CAP": vector_number,
                                     }
                                     )
        fields = [text, text_embedding]

        # Check if index exists
        try:
            self.redis_client.ft(INDEX_NAME).info()
            print("Index already exists")
        except:
            # Create RediSearch Index
            self.redis_client.ft(INDEX_NAME).create_index(
                fields=fields,
                definition=IndexDefinition(
                    prefix=[PREFIX], index_type=IndexType.HASH)
            )

        for embedding in embeddings:
            key = f"{PREFIX}:{str(embedding['id'])}"
            embedding["vector"] = np.array(
                embedding["vector"], dtype=np.float32).tobytes()
            self.redis_client.hset(key, mapping=embedding)
        print(
            f"Loaded {self.redis_client.info()['db0']['keys']} documents in Redis search index with name: {INDEX_NAME}")


    def search_fact(self,
                     user_query: str,
                     index_name: str = "embeddings-index",
                     vector_field: str = "vector",
                     return_fields: list = ["text", "vector_score"],
                     hybrid_fields="*",
                     k: int = 5,
                     print_results: bool = False,
                     ):
        # Creates embedding vector from user query
        embedded_query = client.embeddings.create(input=user_query,
                                                 model="text-embedding-ada-002").data[0].embedding
        # Prepare the Query
        base_query = f'{hybrid_fields}=>[KNN {k} @{vector_field} $vector AS vector_score]'
        query = (
            Query(base_query)
            .return_fields(*return_fields)
            .sort_by("vector_score")
            .paging(0, k)
            .dialect(2)
        )
        params_dict = {"vector": np.array(
            embedded_query).astype(dtype=np.float32).tobytes()}
        # perform vector search
        results = self.redis_client.ft(index_name).search(query, params_dict)
        if print_results:
            for i, doc in enumerate(results.docs):
                score = 1 - float(doc.vector_score)
                print(f"search result {i}: {doc.text} (Score: {round(score ,3) })")
        return [doc['text'] for doc in results.docs]
