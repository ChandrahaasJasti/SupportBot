# Bot - RAG-Powered Document Assistant

## Overview
This project implements a Retrieval-Augmented Generation (RAG) system that automatically processes documents and provides intelligent query responses using vector similarity search.

## RAG System Abstraction

### How It Works
The RAG system automatically processes documents in the "DOCS" folder and stores vector embeddings in the "FAISS" directory whenever you create an object of the `EmbRag` class-> You need to pass the directory paths of DOCS and FAISS into the object. Simply use the `queryDB()` method to retrieve the top 3 most relevant document chunks for any query.

### Supported Document Types
The DOCS folder supports multiple file formats:
- **PDF files** (.pdf) - Automatically converted to markdown
- **Word documents** (.docx) - Text extraction
- **Markdown files** (.md) - Direct processing
- **Text files** (.txt) - Plain text processing
- **Web URLs** - Must be stored in a file named exactly "urls.txt" containing comma-separated URLs

### Basic Usage
```python
from utils.rag import EmbRag

# Initialize RAG system
rag = EmbRag(docs_path="path/to/DOCS", faiss_path="path/to/FAISS")

# Query documents
answer = rag.queryDB("What is the POC for insurance?")
print(answer)
```

## Internal Working

### Document Processing Pipeline
1. **Initialization**: When `EmbRag` is instantiated, it automatically:
   - Scans the DOCS folder for new/unprocessed files
   - Processes each document based on its type
   - Generates embeddings for text chunks
   - Updates the FAISS index and metadata

2. **Chunking Strategy**: The system uses an intelligent LLM-based chunking approach:
   - Documents are initially split into 256-word blocks
   - For each block, the LLM determines if it contains multiple topics
   - If a second topic is detected, the block is split at the topic boundary
   - First part becomes a finalized chunk, second part is prepended to the next block
   - This ensures semantic coherence within each chunk

3. **Embedding Generation**: 
   - Uses Ollama's nomic-embed-text model for generating embeddings
   - Embeddings are L2-normalized for optimal similarity search
   - Stored in FAISS index for fast retrieval

### File Structure

#### `cache.json`
- **Purpose**: Tracks which documents have been processed
- **Format**: JSON mapping of filename to processing status
- **Example**:
```json
{
    "RAG_DOC.pdf": "True",
    "McaaS_Documentation.pdf": "True"
}
```

#### `meta_data.json`
- **Purpose**: Stores all document chunks with metadata
- **Format**: JSON array of chunk objects
- **Structure**:
```json
[
    {
        "doc": "filename.pdf",
        "id": 0,
        "content": "chunk text content..."
    }
]
```

#### `index.bin`
- **Purpose**: FAISS vector index containing all document embeddings
- **Type**: Binary FAISS index file (IndexFlatL2 with 768 dimensions)
- **Usage**: Enables fast similarity search for query vectors

### Query Process
1. **Query Enhancement**: User query is enhanced using LLM-based query expansion
2. **Vector Search**: Enhanced query is embedded and searched against FAISS index
3. **Top-K Retrieval**: Returns top 3 most similar chunks based on L2 distance
4. **Summarization**: Retrieved chunks are summarized using LLM to provide coherent answers
5. **Response**: Final answer is returned to the user

### Performance Features
- **Caching**: Only processes new/unmodified documents
- **Incremental Updates**: FAISS index is updated incrementally
- **Efficient Search**: Vector similarity search for sub-second response times
- **Smart Chunking**: LLM-guided chunking ensures semantic coherence

## Technical Requirements
- Python 3.10+
- Ollama running locally with nomic-embed-text model
- Required packages: faiss-cpu, pymupdf4llm, trafilatura, numpy, requests
- Google Gemini API key for LLM operations

## Architecture Benefits
- **Automatic Processing**: No manual intervention required for new documents
- **Scalable**: Handles multiple document types and formats
- **Intelligent**: LLM-guided chunking and query enhancement
- **Fast**: Vector similarity search for quick responses
- **Persistent**: Maintains state across sessions via cache and index files
