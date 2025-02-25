import networkx as nx

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
