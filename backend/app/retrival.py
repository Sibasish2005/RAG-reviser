from app.embeding import create_embeddings
from app.vector_store import client, COLLECTION_NAME


def retrieve(query, limit=5):

    query_embedding = create_embeddings([query])[0]

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding.tolist(),
        limit=limit,
    )

    return results.points