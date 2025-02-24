import networkx as nx

PartialOrder = list[tuple[int, int]]
CoverRelation = list[tuple[int, int]]
LinearOrder = str
AcyclicDiGraph = nx.DiGraph
HasseDiagram = nx.DiGraph
AnchorPair = tuple[int, int]
EdgeLabel = frozenset[int, int]
AdjacentTranspositionGraph = nx.Graph

# not the same as upsilon: list[LinearOrder] as LinearExtensions must correspond to a poset
LinearExtensions = list[LinearOrder]
