import json
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

import plotly.graph_objects as go
import plotly.io as pio

from backend.app.posetvisualizer import PosetVisualizer
from backend.app.posetsolver import PosetSolver
from backend.app.posetutils import PosetUtils


class GraphRequest(BaseModel):
    sequence: str
    selected_nodes: Optional[list[str]] = []
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
    allow_origin_regex="https://atg-visualizer-.*\.vercel\.app",  # type: ignore
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/graph", response_model=GraphData)
def get_graph(
    size: int,
    selected_nodes: list[str] = Query(None),
    highlighted_nodes: list[str] = Query(None),
):
    try:
        if size < 2 or size > PosetVisualizer.MAX_SIZE:
            raise ValueError(f"Size must be between 2 and {PosetVisualizer.MAX_SIZE}.")

        visualizer = PosetVisualizer(size)

        if selected_nodes and highlighted_nodes:
            visualizer.select_and_highlight_nodes(
                select_nodes=selected_nodes, highlight_nodes=highlighted_nodes
            )
        elif selected_nodes:
            visualizer.select_nodes(select_nodes=selected_nodes)

        fig_data = visualizer.get_figure_data()

        return JSONResponse(content=pio.to_json(fig_data))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/solve")
def solve_optimal_k_poset_cover(k: int, upsilon: list[str] = Query([])):
    try:
        print(f"{k = }. k is not handled yet.")
        result_linear_orders = PosetSolver.minimum_poset_cover(upsilon)
        result_posets = [
            PosetUtils.get_partial_order_of_convex(leg) for leg in result_linear_orders
        ]

        return JSONResponse(
            content=json.dumps(
                {
                    "resultPosets": result_posets,
                    "resultLinearOrders": result_linear_orders,
                }
            )
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/health")
def test_health():
    return JSONResponse(content={"message": "good"})
