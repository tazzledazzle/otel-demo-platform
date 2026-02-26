# RAG Overview

RAG stands for Retrieval-Augmented Generation. It combines a retrieval step with a language model to answer questions using your own documents.

First, you turn documents into vectors and store them in a vector database. When a user asks a question, you find the most relevant chunks, then pass them to the LLM as context. This keeps answers grounded in your data and reduces hallucination.
