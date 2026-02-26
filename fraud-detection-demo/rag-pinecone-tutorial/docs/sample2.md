# Vector Embeddings

Embeddings are dense numerical representations of text. Similar pieces of text get similar vectors, so you can find relevant passages by comparing embedding distances.

OpenAI's text-embedding-3-small model produces 1536-dimensional vectors. You chunk your documents, embed each chunk, and upsert the vectors into a store like Pinecone. At query time, you embed the question and search for the nearest vectors.
