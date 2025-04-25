import json
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Literal

import plotly.graph_objects as go
import plotly.io as pio

from app.posetvisualizer import PosetVisualizer
from app.posetsolver import PosetSolver
from app.posetutils import PosetUtils


class GraphRequest(BaseModel):
    input_mode: Literal["Linear Orders", "Poset"]
    drawing_method: Literal[
        "Default",
        "Permutahedron",
        "Supercover",
        "Hexagonal",
        "Supercover + Hexagonal",
        "Hexagonal1",
        "Supercover + Hexagonal 1",
    ]
    size: int
    selected_nodes: list[str] = []
    highlighted_nodes: list[str] = []
    cover_relation: list[tuple[int, int]] = []


class GraphData(BaseModel):
    data: list[go.Scatter3d]
    layout: go.Layout

    class Config:
        arbitrary_types_allowed = True


METHOD_MAP = {
    "Default": (False, False, False, False),
    "Permutahedron": (True, False, False, False),
    "Supercover": (False, True, False, False),
    "Hexagonal": (False, False, True, False),
    "Supercover + Hexagonal": (False, True, True, False),
    "Hexagonal1": (False, False, True, True),
    "Supercover + Hexagonal1": (False, True, True, True),
}


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


@app.post("/graph", response_model=GraphData)
async def get_graph(graphRequest: GraphRequest):
    try:
        if graphRequest.input_mode == "Linear Orders":
            size = graphRequest.size
            drawing_method = graphRequest.drawing_method
            selected_nodes = graphRequest.selected_nodes
            highlighted_nodes = graphRequest.highlighted_nodes

            if size < 2 or size > PosetVisualizer.MAX_SIZE:
                raise ValueError(
                    f"Size must be between 2 and {PosetVisualizer.MAX_SIZE}."
                )

            # visualizer = PosetVisualizer(size)

            if selected_nodes and highlighted_nodes:
                visualizer = PosetVisualizer(
                    size, selected_nodes, *METHOD_MAP[drawing_method], highlighted_nodes
                )
            elif selected_nodes:
                visualizer = PosetVisualizer(
                    size, selected_nodes, *METHOD_MAP[drawing_method]
                )

            fig_data = visualizer.get_figure_data()

            return JSONResponse(content=pio.to_json(fig_data))
        elif graphRequest.input_mode == "Poset":
            size = graphRequest.size
            drawing_method = graphRequest.drawing_method
            cover_relation = graphRequest.cover_relation

            sequence = "".join(map(str, range(1, size + 1)))
            linear_extensions = PosetUtils.get_linear_extensions_from_relation(
                cover_relation, sequence
            )
            visualizer = PosetVisualizer(
                size, linear_extensions, *METHOD_MAP[drawing_method]
            )

            fig_data = visualizer.get_figure_data()
            return JSONResponse(content=pio.to_json(fig_data))
        else:
            raise ValueError(f"Invalid input_mode value.")
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
