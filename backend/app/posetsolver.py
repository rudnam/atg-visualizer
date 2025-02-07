import networkx as nx
from itertools import combinations, product
from typing import List, Tuple
import copy

# MY TYPES
PartialOrder = List[Tuple[int, int]]
CoverRelation = List[Tuple[int, int]]
LinearOrder = str
DiGraph = nx.DiGraph
HasseDiagram = nx.DiGraph
AnchorPair = Tuple[int, int]


class PosetCoverProblem:
    def __init__(self, upsilon, k=None):
        self.upsilon = upsilon
        self.k = k

    def minimum_poset_cover(
        self, upsilon=List[LinearOrder], verbose=False
    ) -> List[List[LinearOrder]]:
        """Find the minimum poset cover. May run in exp time w.r.t. the length of input"""
        n = len(upsilon)
        result = None
        for k in range(1, n + 1):
            if k == 1:
                convex = PosetUtils.generate_convex(upsilon)
                if set(convex) == set(upsilon):
                    result = [convex]
            elif k == n - 1:
                result = upsilon
            else:
                result = self.exact_k_poset_cover(upsilon, k)

            if verbose and result:
                print(f"Found a {k}-poset cover")
                print(f"[RESULT]: {result}")
            elif verbose:
                print(f"Failed to find a {k}-poset cover")

            if result:
                break

        return result if result else []

    def exact_k_poset_cover(
        self, upsilon: List[LinearOrder], k: int, verbose=False
    ) -> List[List[LinearOrder]] | None:
        """Find a k-poset cover given upsilon. Static method."""

        if verbose:
            print(f"Input k = {k}")
            print(f"Upsilon={upsilon}\n")

        if k == 1:
            convex = PosetUtils.generate_convex(upsilon)
            if set(convex) == set(upsilon):
                return convex
            return None

        atg_edges = set()  # type. set of Tuple[int,int]

        for i in range(len(upsilon)):
            for j in range(i + 1, len(upsilon)):
                edge = PosetUtils.edge_label(upsilon[i], upsilon[j])
                if edge:
                    atg_edges.add((int(edge[0]), int(edge[1])))
                    atg_edges.add((int(edge[1]), int(edge[0])))

        if verbose:
            print(f"ATG Edges (directed): {atg_edges}\n")

        A_star = combinations(atg_edges, k - 1)
        legs = []
        for anchor_pairs in A_star:
            Y_A = set()
            for linear_order in upsilon:
                linear_order_follows_anchor_pairs = all(
                    [
                        PosetUtils.x_is_less_than_y_in_L(linear_order, a, b)
                        for a, b in anchor_pairs
                    ]
                )
                if linear_order_follows_anchor_pairs:
                    Y_A.add(linear_order)

            A_is_a_poset = False
            partial_order_A = None
            if Y_A:
                partial_order_A = PosetUtils.get_partial_order_of_convex(Y_A)
                A_is_a_poset = (
                    set(
                        PosetUtils.get_linear_extensions_from_relation(
                            partial_order_A, upsilon[0]
                        )
                    )
                    == Y_A
                )

            if verbose:
                print(f"anchors: {anchor_pairs}")
                print(f"Y_A: {Y_A}")
                if Y_A:
                    print(f"is_poset: {A_is_a_poset}")

            if A_is_a_poset:
                maximal_supercover_linear_extensions = self.maximal_poset(
                    upsilon, list(anchor_pairs), partial_order_A
                )
                if verbose:
                    print(f"my_super: {maximal_supercover_linear_extensions}")
                legs.append(maximal_supercover_linear_extensions)
            if verbose:
                print("")

        if verbose:
            print("------------------------[LEGs Collected]---------------------------")
            for leg in legs:
                print(leg)
        if verbose:
            print("-------------------------------------------------------------------")

        for solution in combinations(legs, k):
            sets_in_solution = [set(leg) for leg in solution]
            if set.union(*sets_in_solution) == set(upsilon):
                if verbose:
                    print(f"\n[RESULT]: {list(solution)}")
                return list(solution)
        return None

    def maximal_poset(
        self,
        upsilon: List[LinearOrder],
        anchor_pairs: List[AnchorPair],
        partial_order: PartialOrder,
        verbose=False,
    ) -> List[LinearOrder]:
        """
        Input: A set Y of linear orders, a set A of anchor pairs, and a poset P_A whose linear extensions are bounded by A,
            i.e L(P) subseteq Y and A subseteq P_A
        I.e. the following must hold:
            get_linear_extensions_from_relation(partial_order) is a subseteq of upsilon, and
            anchor_pairs is a subseteq of partial_order
        """

        if verbose:
            print("Input")
            print(f"upsilon:       {upsilon}")
            print(f"anchor_pairs:  {anchor_pairs}")
            print(f"partial_order: {partial_order}\n")

        upsilon = set(upsilon)
        partial_order = set(partial_order)

        Y_covered = set(
            PosetUtils.get_linear_extensions_from_relation(
                partial_order, list(upsilon)[0]
            )
        )
        Y_uncovered = {
            linear_order for linear_order in upsilon if linear_order not in Y_covered
        }
        hasse = PosetUtils.get_hasse_from_partial_order(partial_order, list(upsilon)[0])

        J_sets = [
            set(
                product(
                    PosetUtils.ancestors(a, hasse) | {a},
                    PosetUtils.descendants(b, hasse) | {b},
                )
            )
            for a, b in anchor_pairs
        ]
        J = list(set.union(*J_sets))
        J.sort(key=lambda anchor_pair: PosetUtils.hasse_dist(hasse, *anchor_pair))

        I = copy.deepcopy(J)
        if verbose:
            print(f"Anchor Pairs ranked by distance, I: {I}")

        current_pair = I[0]
        pair_index = 0
        blacklist = set()
        while True:
            x, y = current_pair
            L = {
                linear_order
                for linear_order in Y_covered
                if PosetUtils.x_is_covered_by_y_in_L(linear_order, x=x, y=y)
            }
            L_prime = {
                PosetUtils.swap_xy_in_L(linear_order, x, y) for linear_order in L
            }
            L_prime = {
                linear_order for linear_order in L_prime if linear_order in Y_uncovered
            }

            if verbose:
                print(f"\ncurrent_pair: {x} {y}")
                print(f"Y_covered:   {Y_covered}")
                print(f"Y_uncovered: {Y_uncovered}")
                print(f"L:           {L}")
                print(f"L_prime:     {L_prime}")

            if len(L) == len(L_prime) and len(L) != 0:
                convex_of_L_prime = set(PosetUtils.generate_convex(list(L_prime)))
                if convex_of_L_prime <= upsilon:
                    partial_order -= {(x, y)}
                    Y_covered |= convex_of_L_prime
                    Y_uncovered -= convex_of_L_prime
                else:
                    blacklist |= set(
                        product(
                            PosetUtils.ancestors(x, hasse),
                            PosetUtils.descendants(y, hasse),
                        )
                    )
            else:
                blacklist |= set(
                    product(
                        PosetUtils.ancestors(x, hasse), PosetUtils.descendants(y, hasse)
                    )
                )

            if verbose:
                print(f"blacklist: {blacklist}")

            prev_pair = (x, y)

            pair_index += 1
            current_pair = None if pair_index >= len(I) else I[pair_index]
            while current_pair in blacklist:
                pair_index += 1
                current_pair = None if pair_index >= len(I) else I[pair_index]
            if (
                current_pair is None
                or PosetUtils.hasse_dist(hasse, *current_pair)
                - PosetUtils.hasse_dist(hasse, *prev_pair)
                > 1
            ):
                break

        if verbose:
            print(f"\n[RESULT]: {list(Y_covered)}")
        return list(Y_covered)


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
