import numpy as np

DOCUMENT_CHUNKS = []
DOCUMENT_EMBEDDINGS = []


def store_document(chunks, embeddings):

    global DOCUMENT_CHUNKS
    global DOCUMENT_EMBEDDINGS

    DOCUMENT_CHUNKS = chunks
    DOCUMENT_EMBEDDINGS = embeddings


def search(query_embedding, top_k: int = 1):

    similarities = []

    for embedding in DOCUMENT_EMBEDDINGS:

        similarity = np.dot(query_embedding, embedding) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(embedding)
        )

        similarities.append(similarity)

    best_index = int(np.argmax(similarities))

    return DOCUMENT_CHUNKS[best_index]
