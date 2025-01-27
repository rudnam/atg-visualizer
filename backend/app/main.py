from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional

import plotly.graph_objects as go
import plotly.io as pio

from app.graph import MAX_SIZE, PosetSolver


class GraphRequest(BaseModel):
    sequence: str
    selected_nodes: Optional[List[str]] = []
    opacity_others: Optional[float] = 0.1


class GraphData(BaseModel):
    data: list[go.Scatter3d]
    layout: go.Layout

    class Config:
        arbitrary_types_allowed = True


app = FastAPI()

origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "https://atg-visualizer.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/graph", response_model=GraphData)
def get_graph(
    size: int,
    selected_nodes: List[str] = Query(None),
    opacity_others: float = 0.1,
):
    try:
        if size < 2 or size > MAX_SIZE:
            raise ValueError(f"Size must be between 2 and {MAX_SIZE}.")

        solver = PosetSolver(size)
        fig_data = solver.get_figure_data()

        return JSONResponse(content=pio.to_json(fig_data))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/health")
def test_health():
    return JSONResponse(content={"message": "good"})
