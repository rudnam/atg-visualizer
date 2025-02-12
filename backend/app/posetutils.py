from app.classes import *


class PosetUtils:
    @staticmethod
    def get_linear_extensions_from_graph(
        G: DiGraph | HasseDiagram,
    ) -> List[LinearOrder]:
        sortings = list(nx.all_topological_sorts(G))
        return sorted(["".join(map(str, sorting)) for sorting in sortings])

    @staticmethod
    def get_linear_extensions_from_relation(
        relation: PartialOrder | CoverRelation, sequence: str
    ) -> List[LinearOrder]:
        G = nx.DiGraph()
        G.add_nodes_from(range(1, len(sequence) + 1))
        G.add_edges_from(relation)
        sortings = list(nx.all_topological_sorts(G))
        return sorted(["".join(map(str, sorting)) for sorting in sortings])

    @staticmethod
    def get_graph_from_relation(
        relation: PartialOrder | CoverRelation, sequence: str
    ) -> nx.DiGraph:
        G = nx.DiGraph()
        G.add_nodes_from(range(1, len(sequence) + 1))
        G.add_edges_from(relation)
        return G

    @staticmethod
    def get_hasse_from_partial_order(
        partial_order: PartialOrder, sequence: str
    ) -> HasseDiagram:
        G = nx.DiGraph()
        G.add_nodes_from(range(1, len(sequence) + 1))
        G.add_edges_from(partial_order)
        TR = nx.transitive_reduction(G)
        return TR

    @staticmethod
    def ancestors(node: int, G: DiGraph | HasseDiagram) -> set[int]:
        """Used in the Algo: nx.ancestors(hasse, 4) | {4}"""
        return nx.ancestors(G, node)

    @staticmethod
    def descendants(node: int, G: DiGraph | HasseDiagram) -> set[int]:
        """Used in the Algo: nx.descendants(hasse, 1) | {1}"""
        return nx.descendants(G, node)

    @staticmethod
    def hasse_dist(hasse: HasseDiagram, node1: int, node2: int) -> int | float:
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
        """True if node1 is covered by node2"""
        return node2 in hasse.successors(node2)

    @staticmethod
    def x_is_covered_by_y_in_L(linear_order: LinearOrder, x: int, y: int) -> bool:
        x_index = linear_order.find(str(x))
        x_is_found_and_not_last = x_index not in [-1, len(linear_order) - 1]
        return x_is_found_and_not_last and linear_order[x_index + 1] == str(y)

    @staticmethod
    def x_is_less_than_y_in_L(linear_order: LinearOrder, x: int, y: int) -> bool:
        i = linear_order.find(str(x))
        j = linear_order.find(str(y))
        return i != -1 and j != -1 and i < j

    @staticmethod
    def swap_xy_in_L(linear_order: LinearOrder, x: int, y: int) -> LinearOrder:
        """Warning. x must come before y in the linear order"""
        x_index = linear_order.find(str(x))
        if linear_order[x_index + 1] != str(y):
            raise ValueError(
                f"{y} does not immediately succeed {x}. linear_order={linear_order}"
            )
        return f"{linear_order[:x_index]}{str(y)}{str(x)}{linear_order[x_index+2:]}"

    @staticmethod
    def edge_label(linear_order1: str, linear_order2: str) -> Tuple[int, int]:
        """
        Returns the two numbers that were swapped between permutations,
        or None if not a valid adjacent transposition
        """
        p1 = linear_order1
        p2 = linear_order2
        if len(p1) != len(p2):
            return None

        diff_positions = [i for i in range(len(p1)) if p1[i] != p2[i]]

        if len(diff_positions) != 2:
            return None

        pos1, pos2 = diff_positions
        if abs(pos1 - pos2) != 1:
            return None

        if p1[pos1] != p2[pos2] or p1[pos2] != p2[pos1]:
            return None

        return tuple(sorted([p1[pos1], p1[pos2]]))

    @staticmethod
    def generate_convex(linear_orders: List[LinearOrder]) -> List[LinearOrder]:
        if not linear_orders:
            raise ValueError(
                f"Cannot get conv(L) if L is empty. linear_orders={linear_orders}"
            )

        partial_order = PosetUtils.get_partial_order_of_convex(linear_orders)
        supercover = PosetUtils.get_linear_extensions_from_relation(
            partial_order, sequence=linear_orders[0]
        )
        return supercover

    @staticmethod
    def get_partial_order_of_convex(linear_orders: List[LinearOrder]) -> PartialOrder:
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
