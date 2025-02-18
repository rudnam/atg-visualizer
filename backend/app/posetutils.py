from app.classes import *


class PosetUtils:
    @staticmethod
    def get_atg_from_upsilon(upsilon: List[LinearOrder]):
        """Get the Adjacent Transposition Graph of upsilon.
        
        Parameters \\
        upsilon (required) -- a list of linear orders. Linear orders must have equal lengths.

        Returns \\
        nx.Graph
        """
        G = nx.Graph()
        G.add_nodes_from(upsilon)
        for i in range(len(upsilon)):
            for j in range(i + 1, len(upsilon)):
                swapped_nums = PosetUtils.edge_label(upsilon[i], upsilon[j])
                if swapped_nums:
                    G.add_edge(upsilon[i], upsilon[j])
        return G

    @staticmethod
    def get_linear_extensions_from_graph(
        G: AcyclicDiGraph | HasseDiagram,
    ) -> List[LinearOrder]:
        """Get the linear extensions of a poset using either its hasse or directed acyclic graph representation.

        Returns a list of linear orders like ['1234','2134'].

        Parameters \\
        G (required) -- a graph representation of the poset, either hasse or DAG, which are both nx.DiGraph

        Returns \\
        List[LinearOrder] aka List[str]
        """
        sortings = list(nx.all_topological_sorts(G))
        return sorted(["".join(map(str, sorting)) for sorting in sortings])

    @staticmethod
    def get_linear_extensions_from_relation(
        relation: PartialOrder | CoverRelation, sequence: str
    ) -> List[LinearOrder]:
        """Get the linear extensions of a poset using either its partial order or cover relation.

        Returns a list of linear orders like ['1234','2134'].

        Parameters \\
        relation (required) -- the partial order or cover relation of a poset, e.g. [(1,2),(2,3)] \\
        sequence (required) -- a sample linear order like '1234'. The relation can sometimes \\
            not include all the nodes of a poset, like in the example above, what if 4 is also a node? \\
            This ensures that ['1234','1243','1423','4123'] is returned and not ['123']

        Returns \\
        List[LinearOrder] aka List[str]
        """
        G = nx.DiGraph()
        G.add_nodes_from(range(1, len(sequence) + 1))
        G.add_edges_from(relation)
        sortings = list(nx.all_topological_sorts(G))
        return sorted(["".join(map(str, sorting)) for sorting in sortings])

    @staticmethod
    def get_graph_from_relation(
        relation: PartialOrder | CoverRelation, sequence: str
    ) -> AcyclicDiGraph | HasseDiagram:
        """Get the directed acyclic graph representation of a poset using either its partial order or cover relation.

        Returns a AcyclicDiGraph aka nx.DiGraph.

        Parameters \\
        relation (required) -- the partial order or cover relation of a poset, e.g. [(1,2),(2,3)] \\
        sequence (required) -- a sample linear order like '1234'. The relation can sometimes \\
            not include all the nodes of a poset, like in the example above, what if 4 is also a node? \\
            This ensures that all four nodes are present in the graph and not just three.

        Returns \\
        AcyclicDiGraph aka nx.DiGraph
        """
        G = nx.DiGraph()
        G.add_nodes_from(range(1, len(sequence) + 1))
        G.add_edges_from(relation)
        return G

    @staticmethod
    def get_hasse_from_partial_order(
        partial_order: PartialOrder, sequence: str
    ) -> HasseDiagram:
        """Get the hasse representation of a poset using its partial order.

        Returns a HasseDiagram aka nx.DiGraph.

        Parameters \\
        partial_order (required) -- the partial order of a poset, e.g. [(1,2),(2,3)]. \\
            Providing the cover relation of the poset instead will still result in \\
            the correct output as the the cover relation is already transitively reduced. \\
        sequence (required) -- a sample linear order like '1234'. The relation can sometimes \\
            not include all the nodes of a poset, like in the example above, what if 4 is also a node? \\
            This ensures that all four nodes are present in the graph and not just three.

        Returns \\
        HasseDiagram aka nx.DiGraph
        """
        G = nx.DiGraph()
        G.add_nodes_from(range(1, len(sequence) + 1))
        G.add_edges_from(partial_order)
        TR = nx.transitive_reduction(G)
        return TR

    @staticmethod
    def ancestors(node: int, G: AcyclicDiGraph | HasseDiagram) -> set[int]:
        """Get the ancestors of a node given the hasse or directed acyclic graph representation of a poset.

        Returns a set of node names like {1, 2, 3, 4}.

        Parameters \\
        node (required) -- the name of the node \\
        G (required) -- a graph representation of the poset, either hasse or DAG, which are both nx.DiGraph

        Returns \\
        Set[int]

        Notes \\
        Example use case in the algorithm: \\
        nx.ancestors(hasse, 4) | {4}
        """
        return nx.ancestors(G, node)

    @staticmethod
    def descendants(node: int, G: AcyclicDiGraph | HasseDiagram) -> set[int]:
        """Get the descendants of a node given the hasse or directed acyclic graph representation of a poset.

        Returns a set of node names like {1, 2, 3, 4}.

        Parameters \\
        node (required) -- the name of the node \\
        G (required) -- a graph representation of the poset, either hasse or DAG, which are both nx.DiGraph

        Returns \\
        Set[int]

        Notes \\
        Example use case in the algorithm: \\
        nx.descendants(hasse, 1) | {1}
        """
        return nx.descendants(G, node)

    @staticmethod
    def hasse_dist(hasse: HasseDiagram, node1: int, node2: int) -> int | float:
        """Get the distance between two nodes in the hasse representation of a poset.

        Returns int if any of the nodes can be reached from the other, float(-inf) if not.
        
        Parameters \\
        hasse (required) -- the hasse representation of a poset of type HasseDiagram aka nx.DiGraph \\
        node1 (required) -- the name of a node \\
        node2 (required) -- the other node; order does not matter
        
        Returns \\
        int | float

        Raises \\
        Warning. Does not catch the error if any of the nodes are not in the graph.
        """
        from_node1 = float("inf")
        from_node2 = float("inf")
        try:
            from_node1 = nx.shortest_path_length(hasse, node1, node2)
        except nx.NetworkXNoPath:
            pass
        try:
            from_node2 = nx.shortest_path_length(hasse, node2, node1)
        except nx.NetworkXNoPath:
            pass
        return min(from_node1, from_node2)

    @staticmethod
    def covers(hasse: HasseDiagram, node1: int, node2: int) -> bool:
        """Return true if node1 is covered by node2.
        
        Parameters \\
        hasse (required) -- the hasse representation of a poset of type HasseDiagram aka nx.DiGraph \\
        node1 (required) -- the name of the covered node \\
        node2 (required) -- the name of the covering node

        Returns \\
        bool

        Raises \\
        Errors should not be handled.
        """
        return node2 in hasse.successors(node1)

    @staticmethod
    def x_is_covered_by_y_in_L(linear_order: LinearOrder, x: int, y: int) -> bool:
        """Return true if x and y are adjacent in a linear order, in order.

        Example: x=3, y=4, linear_order='12345' => True

        Parameters \\
        linear_order (required) -- \\
        x (required) -- \\
        y (required) -- \\
        
        Returns \\
        bool
        """
        x_index = linear_order.find(str(x))
        x_is_found_and_not_last = x_index not in [-1, len(linear_order) - 1]
        return x_is_found_and_not_last and linear_order[x_index + 1] == str(y)

    @staticmethod
    def x_is_less_than_y_in_L(linear_order: LinearOrder, x: int, y: int) -> bool:
        """Return true if x comes before y in a linear order.

        Example: x=3, y=4, linear_order='12345' => True

        Parameters \\
        linear_order (required) -- \\
        x (required) -- \\
        y (required) -- \\
        
        Returns \\
        bool
        """
        i = linear_order.find(str(x))
        j = linear_order.find(str(y))
        return i != -1 and j != -1 and i < j

    @staticmethod
    def swap_xy_in_L(linear_order: LinearOrder, x: int, y: int) -> LinearOrder:
        """Swap two adjacent nodes in a linear order. Order matters in the input; x must come before y.
        
        Parameters \\
        linear_order (required) -- \\
        x (required) -- \\
        y (required) -- \\

        Returns \\
        LinearOrder aka str
        """
        x_index = linear_order.find(str(x))
        if linear_order[x_index + 1] != str(y):
            raise ValueError(
                f"{y} does not immediately succeed {x}. linear_order={linear_order}"
            )
        return f"{linear_order[:x_index]}{str(y)}{str(x)}{linear_order[x_index+2:]}"

    @staticmethod
    def edge_label(linear_order1: str, linear_order2: str) -> EdgeLabel | None:
        """
        Returns the two numbers that were swapped between permutations,
        or None if not a valid adjacent transposition
        """
        p1 = linear_order1
        p2 = linear_order2
        if len(p1) != len(p2):
            raise ValueError(
                f"Linear orders must have equal lengths. Received {linear_order1=}, {linear_order2=}"
            )

        diff_positions = [i for i in range(len(p1)) if p1[i] != p2[i]]

        if len(diff_positions) != 2:
            return None

        pos1, pos2 = diff_positions
        if abs(pos1 - pos2) != 1:
            return None

        if p1[pos1] != p2[pos2] or p1[pos2] != p2[pos1]:
            return None

        x = int(p1[pos1])
        y = int(p1[pos2])
        return frozenset({x, y})

    @staticmethod
    def generate_convex(linear_orders: List[LinearOrder]) -> List[LinearOrder]:
        """Get the smallest convex set of linear orders which contains the input.
        
        Parameters \\
        linear_orders (required) -- \\
        
        Returns \\
        List[LinearOrder] aka List[str]
        """
        if not linear_orders:
            raise ValueError(
                f"Cannot get conv(L) if L is empty. linear_orders={linear_orders}"
            )

        if len(linear_orders) == 1:
            return linear_orders

        partial_order = PosetUtils.get_partial_order_of_convex(linear_orders)
        supercover = PosetUtils.get_linear_extensions_from_relation(
            partial_order, sequence=linear_orders[0]
        )
        return supercover

    @staticmethod
    def get_partial_order_of_convex(linear_orders: List[LinearOrder]) -> PartialOrder:
        """Get the partial order which describes the smallest convex set of linear orders which contains the input.
        
        Parameters \\
        linear_orders (required) -- 
        
        Returns \\
        PartialOrder aka List[Tuple[int,int]]
        """
        if not linear_orders:
            raise ValueError(
                f"Cannot get conv(L) if L is empty. linear_orders={linear_orders}"
            )

        def get_partial_order(linear_order: str) -> set:
            partial_order = set()
            n = len(linear_order)
            for i in range(n):
                for j in range(i + 1, n):
                    partial_order.add((int(linear_order[i]), int(linear_order[j])))
            return partial_order

        partial_orders = [get_partial_order(l) for l in linear_orders]
        if len(partial_orders) == 0:
            return []
        return list(set.intersection(*partial_orders))
