from typing import List
from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from sqlmodel import Session
from pathlib import Path

from .db import create_db_and_tables, get_session
from .models import TodoCreate, TodoRead, TodoUpdate, Todo
from . import crud

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time

# Create FastAPI app
app = FastAPI(title="Minimal Todo API", version="1.0.0")

# Allow local dev tools (Swagger, REST clients)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus metrics
REQUEST_COUNT = Counter(
    'app_requests_total', 
    'Total request count',
    ['method', 'endpoint', 'status']
)
REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds',
    'Request latency in seconds',
    ['method', 'endpoint']
)

@app.middleware("http")
async def metrics_middleware(request, call_next):
    """Track request metrics."""
    start_time = time.time()
    
    response = await call_next(request)
    
    # Calculate latency
    latency = time.time() - start_time
    
    # Record metrics
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(latency)
    
    return response

# Run DB migrations/creation at startup
@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()

# Metrics endpoint for Prometheus
@app.get("/metrics", include_in_schema=False)
def metrics():
    """Expose Prometheus metrics."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

# ✅ Serve index.html at root
@app.get("/", include_in_schema=False)
def root():
    return FileResponse(Path(__file__).parent / "index.html")

# Health check endpoint
@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

# Create todo
@app.post("/todos", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate, session: Session = Depends(get_session)) -> TodoRead:
    return crud.create_todo(session, todo)

# List todos
@app.get("/todos", response_model=List[TodoRead])
def read_todos(session: Session = Depends(get_session)) -> List[TodoRead]:
    return crud.list_todos(session)

# Get todo by id
@app.get("/todos/{todo_id}", response_model=TodoRead)
def read_todo(todo_id: int, session: Session = Depends(get_session)) -> TodoRead:
    return crud.get_todo_or_404(session, todo_id)

# Update todo by id
@app.patch("/todos/{todo_id}", response_model=TodoRead)
def patch_todo(todo_id: int, patch: TodoUpdate, session: Session = Depends(get_session)) -> TodoRead:
    return crud.update_todo(session, todo_id, patch)

# Delete todo by id
@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_todo(todo_id: int, session: Session = Depends(get_session)) -> Response:
    crud.delete_todo(session, todo_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
