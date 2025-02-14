import networkx as nx
from typing import List, Tuple

PartialOrder = List[Tuple[int, int]]
CoverRelation = List[Tuple[int, int]]
LinearOrder = str
AcyclicDiGraph = nx.DiGraph
HasseDiagram = nx.DiGraph
AnchorPair = Tuple[int, int]
