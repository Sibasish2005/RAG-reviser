from app.youtube import transcribe
from app.chunking import chunk_text
from app.embeding import create_embeddings
from app.vector_store import create_collection, store_chunks
from app.retrival import retrieve
from app.llm import generate_answer


# ==========================================
# 1. VIDEO
# ==========================================

url = "https://youtu.be/bm_0jH5ve8U"


# ==========================================
# 2. TRANSCRIPTION
# ==========================================

print("\nFetching transcript...")

transcript = transcribe(url)

print("Transcript fetched.")


# ==========================================
# 3. CHUNKING
# ==========================================

print("\nCreating chunks...")

chunks = chunk_text(transcript)

print(f"Created {len(chunks)} chunks.")


# ==========================================
# 4. EMBEDDINGS
# ==========================================

print("\nCreating embeddings...")

embeddings = create_embeddings(chunks)

print(f"Created {len(embeddings)} embeddings.")
print(f"Embedding dimensions: {len(embeddings[0])}")


# ==========================================
# 5. QDRANT
# ==========================================

print("\nChecking Qdrant collection...")

create_collection()

print("Storing chunks in Qdrant...")

store_chunks(chunks, embeddings)


# ==========================================
# 6. USER QUERY
# ==========================================

query = input("\nAsk your question: ")


# ==========================================
# 7. RETRIEVAL
# ==========================================

print("\nSearching relevant lecture content...")

results = retrieve(query)

print(f"Found {len(results)} relevant chunks.")


# ==========================================
# 8. BUILD CONTEXT
# ==========================================

context = "\n\n".join(
    result.payload["text"]
    for result in results
)


# ==========================================
# 9. LLM STREAMING
# ==========================================

print("\n================ ANSWER ================\n")

for chunk in generate_answer(query, context):
    print(chunk, end="", flush=True)

print("\n")


# ==========================================
# 10. SOURCES
# ==========================================

print("\n================ SOURCES ================\n")

for i, result in enumerate(results, start=1):

    print(f"\nSource {i}")
    print(f"Score: {result.score}")
    print(result.payload["text"][:300])
    print()
