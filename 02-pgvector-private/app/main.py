# main.py - Private RAG Application with pgvector + Ollama
# 100% Self-hosted, No data leaves your infrastructure

import os
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import RealDictCursor
from pgvector.psycopg2 import register_vector
from sentence_transformers import SentenceTransformer
import ollama

# Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://raguser:changeme@localhost:5432/ragdb")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3")

# Initialize
app = FastAPI(
    title="Private RAG API",
    description="Self-hosted RAG with pgvector + Ollama - Swiss Data Compliant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load embedding model (runs locally)
print(f"Loading embedding model: {EMBEDDING_MODEL}")
embedder = SentenceTransformer(EMBEDDING_MODEL)
print("Embedding model loaded!")

# Ollama client
ollama_client = ollama.Client(host=OLLAMA_HOST)


# Models
class Query(BaseModel):
    question: str
    top_k: int = 3
    session_id: Optional[str] = None

class Document(BaseModel):
    content: str
    metadata: Optional[dict] = None

class SearchResult(BaseModel):
    id: int
    content: str
    score: float
    metadata: Optional[dict] = None

class RAGResponse(BaseModel):
    answer: str
    sources: List[SearchResult]


@contextmanager
def get_db():
    """Database connection context manager"""
    conn = psycopg2.connect(DATABASE_URL)
    register_vector(conn)
    try:
        yield conn
    finally:
        conn.close()


def get_embedding(text: str) -> List[float]:
    """Generate embedding using local model"""
    return embedder.encode(text).tolist()


def search_documents(query: str, top_k: int = 3) -> List[SearchResult]:
    """Search documents using pgvector similarity search"""
    query_embedding = get_embedding(query)
    
    with get_db() as conn:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT 
                id,
                content,
                metadata,
                1 - (embedding <=> %s::vector) as similarity
            FROM documents
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        """, (query_embedding, query_embedding, top_k))
        
        results = []
        for row in cur.fetchall():
            results.append(SearchResult(
                id=row['id'],
                content=row['content'],
                score=float(row['similarity']),
                metadata=row['metadata']
            ))
        
        return results


def generate_answer(question: str, context: str) -> str:
    """Generate answer using Ollama (local LLM)"""
    system_prompt = """You are a helpful assistant that answers questions based on the provided context.
Always cite your sources. If you cannot find the answer in the context, say so.
Answer in the same language as the question."""
    
    prompt = f"""Context:
{context}

Question: {question}

Answer:"""
    
    response = ollama_client.chat(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response['message']['content']


@app.get("/")
async def root():
    return {
        "service": "Private RAG API",
        "embedding_model": EMBEDDING_MODEL,
        "llm_model": LLM_MODEL,
        "status": "healthy"
    }


@app.get("/health")
async def health():
    """Health check"""
    try:
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT 1")
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


@app.post("/query", response_model=RAGResponse)
async def query(request: Query):
    """RAG Query - Search and Generate Answer"""
    try:
        # 1. Search relevant documents
        search_results = search_documents(request.question, request.top_k)
        
        if not search_results:
            return RAGResponse(
                answer="No relevant documents found in the knowledge base.",
                sources=[]
            )
        
        # 2. Build context from search results
        context = "\n\n".join([
            f"[Source {i+1}]: {r.content}"
            for i, r in enumerate(search_results)
        ])
        
        # 3. Generate answer using local LLM
        answer = generate_answer(request.question, context)
        
        return RAGResponse(
            answer=answer,
            sources=search_results
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/index")
async def index_document(document: Document):
    """Index a document into pgvector"""
    try:
        embedding = get_embedding(document.content)
        
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO documents (content, metadata, embedding)
                VALUES (%s, %s, %s)
                RETURNING id
            """, (document.content, document.metadata or {}, embedding))
            
            doc_id = cur.fetchone()[0]
            conn.commit()
        
        return {
            "status": "indexed",
            "id": doc_id
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/index/batch")
async def index_batch(documents: List[Document]):
    """Batch index multiple documents"""
    try:
        indexed = []
        
        with get_db() as conn:
            cur = conn.cursor()
            
            for doc in documents:
                embedding = get_embedding(doc.content)
                cur.execute("""
                    INSERT INTO documents (content, metadata, embedding)
                    VALUES (%s, %s, %s)
                    RETURNING id
                """, (doc.content, doc.metadata or {}, embedding))
                
                doc_id = cur.fetchone()[0]
                indexed.append(doc_id)
            
            conn.commit()
        
        return {
            "status": "indexed",
            "count": len(indexed),
            "ids": indexed
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/documents/{doc_id}")
async def delete_document(doc_id: int):
    """Delete a document"""
    try:
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM documents WHERE id = %s", (doc_id,))
            conn.commit()
        
        return {"status": "deleted", "id": doc_id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/documents/count")
async def count_documents():
    """Get document count"""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM documents")
        count = cur.fetchone()[0]
    
    return {"count": count}


@app.get("/models")
async def list_models():
    """List available Ollama models"""
    try:
        models = ollama_client.list()
        return {"models": [m['name'] for m in models['models']]}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
