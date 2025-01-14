from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional

from app.graph import create_graph
import plotly.graph_objects as go
import plotly.io as pio


class GraphRequest(BaseModel):
    sequence: str
    selected_nodes: Optional[List[str]] = []
    opacity_others: Optional[float] = 0.1


app = FastAPI()

origins = ["http://localhost:8080", "https://atg-visualizer.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/graph")
def get_graph(
    sequence: str,
    selected_nodes: Optional[List[str]] = None,
    opacity_others: float = 0.1,
):
    graph_data = create_graph(sequence, selected_nodes, opacity_others)

    graph_json = pio.to_json(graph_data)
    return JSONResponse(content=graph_json)
