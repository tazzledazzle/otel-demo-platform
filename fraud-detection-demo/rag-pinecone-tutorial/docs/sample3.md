# Chunking Strategy

Chunking splits long documents into smaller pieces that fit embedding limits and improve retrieval granularity. Use overlapping chunks so context isn't lost at boundaries.

RecursiveCharacterTextSplitter tries to split on paragraph, then line, then space, keeping sentences intact when possible. A typical setup is chunk_size around 500 characters with chunk_overlap of 50 for continuity between chunks.
