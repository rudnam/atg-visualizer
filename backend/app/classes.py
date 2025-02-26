from typing import TypedDict
import networkx as nx
import plotly.graph_objects as go

type PartialOrder = list[tuple[int, int]]
type CoverRelation = list[tuple[int, int]]
type LinearOrder = str
type AcyclicDiGraph = nx.DiGraph
type HasseDiagram = nx.DiGraph
type AnchorPair = tuple[int, int]
type EdgeLabel = frozenset[int, int]
type AdjacentTranspositionGraph = nx.Graph

# not the same as upsilon: list[LinearOrder] as LinearExtensions must correspond to a poset
type LinearExtensions = list[LinearOrder]


class FigureData(TypedDict):
    data: list[go.Scatter3d]
    layout: go.Layout


class MarkerData(TypedDict):
    color: str
    size: int


class NodeData(TypedDict):
    hoverinfo: str
    marker: MarkerData
    mode: str
    name: str
    opacity: float
    showlegend: bool
    text: str
    textposition: str
    x: float
    y: float
    z: float


class LineData(TypedDict):
    color: str
    width: int


class EdgeData(TypedDict):
    hoverinfo: str
    line: LineData
    mode: str
    name: str
    opacity: float
    showlegend: bool
    x: tuple[float, float]
    y: tuple[float, float]
    z: tuple[float, float]
