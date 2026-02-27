# main.py - Azure RAG Application
# Swiss Data Residency Compliant

import os
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv

from openai import AzureOpenAI
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential

load_dotenv()

app = FastAPI(
    title="Swiss RAG API",
    description="RAG API with Azure OpenAI - Switzerland North",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Azure OpenAI Client
openai_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

# Azure AI Search Client
search_client = SearchClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    index_name=os.getenv("AZURE_SEARCH_INDEX", "documents"),
    credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_API_KEY"))
)

# Models
class Query(BaseModel):
    question: str
    top_k: int = 3

class Document(BaseModel):
    content: str
    metadata: Optional[dict] = None

class SearchResult(BaseModel):
    content: str
    score: float
    metadata: Optional[dict] = None

class RAGResponse(BaseModel):
    answer: str
    sources: List[SearchResult]


def get_embedding(text: str) -> List[float]:
    """Generate embedding using Azure OpenAI"""
    response = openai_client.embeddings.create(
        input=text,
        model=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-ada-002")
    )
    return response.data[0].embedding


def search_documents(query: str, top_k: int = 3) -> List[SearchResult]:
    """Search documents using Azure AI Search with vector search"""
    query_embedding = get_embedding(query)
    
    vector_query = VectorizedQuery(
        vector=query_embedding,
        k_nearest_neighbors=top_k,
        fields="embedding"
    )
    
    results = search_client.search(
        search_text=query,
        vector_queries=[vector_query],
        top=top_k
    )
    
    search_results = []
    for result in results:
        search_results.append(SearchResult(
            content=result.get("content", ""),
            score=result.get("@search.score", 0),
            metadata=result.get("metadata", {})
        ))
    
    return search_results


def generate_answer(question: str, context: str) -> str:
    """Generate answer using Azure OpenAI GPT-4"""
    system_prompt = """You are a helpful assistant that answers questions based on the provided context.
    Always cite your sources. If you cannot find the answer in the context, say so.
    Answer in the same language as the question."""
    
    user_prompt = f"""Context:
{context}

Question: {question}

Answer:"""
    
    response = openai_client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    
    return response.choices[0].message.content


@app.get("/")
async def root():
    return {
        "service": "Swiss RAG API",
        "region": "Switzerland North",
        "status": "healthy"
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/query", response_model=RAGResponse)
async def query(request: Query):
    """RAG Query - Search and Generate Answer"""
    try:
        # 1. Search relevant documents
        search_results = search_documents(request.question, request.top_k)
        
        if not search_results:
            return RAGResponse(
                answer="No relevant documents found.",
                sources=[]
            )
        
        # 2. Build context from search results
        context = "\n\n".join([
            f"[Source {i+1}]: {r.content}"
            for i, r in enumerate(search_results)
        ])
        
        # 3. Generate answer
        answer = generate_answer(request.question, context)
        
        return RAGResponse(
            answer=answer,
            sources=search_results
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/index")
async def index_document(document: Document):
    """Index a document into Azure AI Search"""
    try:
        embedding = get_embedding(document.content)
        
        doc = {
            "id": str(hash(document.content)),
            "content": document.content,
            "embedding": embedding,
            "metadata": document.metadata or {}
        }
        
        result = search_client.upload_documents(documents=[doc])
        
        return {
            "status": "indexed",
            "id": doc["id"],
            "succeeded": result[0].succeeded
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload")
async def upload_file(file: UploadFile):
    """Upload and index a file"""
    try:
        content = await file.read()
        text = content.decode("utf-8")
        
        # Index the document
        embedding = get_embedding(text)
        
        doc = {
            "id": str(hash(text)),
            "content": text,
            "embedding": embedding,
            "metadata": {"filename": file.filename}
        }
        
        result = search_client.upload_documents(documents=[doc])
        
        return {
            "status": "uploaded",
            "filename": file.filename,
            "indexed": result[0].succeeded
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
