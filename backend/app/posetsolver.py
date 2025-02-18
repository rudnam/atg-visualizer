from itertools import combinations, product, chain
from typing import List
import copy

from app.posetutils import PosetUtils
from app.classes import *


class PosetSolver:
    def __init__(self, upsilon, k=None):
        self.upsilon = upsilon
        self.k = k

    def solve(self):
        legs = None
        if self.k and False:
            legs = self.exact_k_poset_cover(self.upsilon, self.k)
            legs = legs if legs else []
        else:
            legs = self.minimum_poset_cover(self.upsilon)
        partial_orders = [PosetUtils.get_partial_order_of_convex(leg) for leg in legs]
        return partial_orders, legs

    def minimum_poset_cover(
        self, upsilon=List[LinearOrder], verbose=False
    ) -> List[List[LinearOrder]] | None:
        G = PosetUtils.get_atg_from_upsilon(upsilon)
        solutions: dict[frozenset[LinearOrder], List[List[LinearOrder]]] = {}
        for connected_component in nx.connected_components(G):
            upsilon1 = list(connected_component)
            solutions[frozenset(connected_component)] = (
                self.minimum_poset_cover_of_connected_component(upsilon1, verbose)
            )
            if verbose:
                print(f'\n{"-"*40}\n')
        poset_cover = list(chain.from_iterable(solutions.values()))
        if verbose:
            print(
                f"Input graph has {len(solutions)} connected component{'s' if len(solutions)>1 else ''}."
            )
            print(f"Combined solution: {poset_cover}")
        return poset_cover

    def minimum_poset_cover_of_connected_component(
        self, upsilon=List[LinearOrder], verbose=False
    ) -> List[List[LinearOrder]] | None:
        """A parameterized algorithm which finds the minimum poset cover"""
        n = len(upsilon)
        result = None
        for k in range(1, n + 1):
            if k == 1:
                convex = PosetUtils.generate_convex(upsilon)
                if set(convex) == set(upsilon):
                    result = [convex]
            elif k == n:
                result = [[linear_order] for linear_order in upsilon]
            else:
                result = self.exact_k_poset_cover(upsilon, k)

            if verbose and result:
                print(f"Found a {k}-poset cover")
                print(f"[RESULT]: {result}")
            elif verbose:
                print(f"Failed to find a {k}-poset cover")

            if result:
                break

        return result

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
