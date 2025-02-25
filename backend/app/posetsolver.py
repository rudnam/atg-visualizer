from itertools import combinations, product, chain
import copy

from app.posetutils import PosetUtils
from app.classes import *


class PosetSolver:
    @staticmethod
    def minimum_poset_cover(
        upsilon: list[LinearOrder], verbose=False
    ) -> list[LinearExtensions]:
        """A parameterized algorithm which finds the minimum poset cover

        Args:
            upsilon: A list of linear orders of equal length
            verbose: Print information while the function executes. Defaults to False.

        Returns:
            list[LinearExtensions]: A list of linear extensions each corresponding to a poset in the poset cover
        """
        atg: AdjacentTranspositionGraph = PosetUtils.get_atg_from_upsilon(upsilon)

        solutions: dict[frozenset[LinearOrder], list[LinearExtensions]] = {}
        for connected_component in nx.connected_components(atg):
            upsilon1: list[LinearOrder] = list(connected_component)
            solutions[frozenset(connected_component)] = (
                PosetSolver._minimum_poset_cover_of_connected_component(
                    upsilon1, verbose
                )
            )

            if verbose:
                print(f'\n{"-"*40}\n')

        poset_cover: list[LinearExtensions] = list(
            chain.from_iterable(solutions.values())
        )

        if verbose:
            print(
                f"Input graph has {len(solutions)} connected component{'s' if len(solutions)>1 else ''}."
            )
            print(f"Combined solution: {poset_cover}")

        return poset_cover

    @staticmethod
    def _minimum_poset_cover_of_connected_component(
        upsilon: list[LinearOrder], verbose=False
    ) -> list[LinearExtensions]:
        """A parameterized algorithm which finds the minimum poset cover (connected)

        The adjacent transposition graph of the input upsilon must be connected.

        Args:
            upsilon: A list of linear orders of equal length
            verbose: Print information while the function executes. Defaults to False.

        Returns:
            list[LinearExtensions]: A list of linear extensions each corresponding to a poset in the poset cover
        """
        n = len(upsilon)
        result: list[LinearExtensions] | None = None
        for k in range(1, n + 1):
            if k == 1:
                convex = PosetUtils.generate_convex(upsilon)
                if set(convex) == set(upsilon):
                    result = [convex]
            elif k == n:
                result = [[linear_order] for linear_order in upsilon]
            else:
                result = PosetSolver.exact_k_poset_cover(upsilon, k)

            if verbose and result:
                print(f"Found a {k}-poset cover")
                print(f"[RESULT]: {result}")
            elif verbose:
                print(f"Failed to find a {k}-poset cover")

            if result is not None:
                break

        assert result is not None
        return result

    @staticmethod
    def exact_k_poset_cover(
        upsilon: list[LinearOrder], k: int, verbose=False
    ) -> list[LinearExtensions] | None:
        """Find k posets which cover the given linear orders

        The adjacent transposition graph of the input upsilon must be connected.
        Restrictions on k. The behavior is set to be undefined if k is not minimal. This includes cases when k-1 is greater than the number of edge classes in the input upsilon.

        Args:
            upsilon: A list of linear orders of equal length
            k: The number of posets to find
            verbose: Print information while the function executes. Defaults to False.

        Returns:
            list[LinearExtensions] | None: A length-k list of linear extensions each corresponding to a poset in the poset cover, if any exists, else returns None
        """

        if verbose:
            print(f"Input k = {k}")
            print(f"Upsilon={upsilon}\n")

        if k == 1:
            convex = PosetUtils.generate_convex(upsilon)
            if set(convex) == set(upsilon):
                return [convex]
            return None

        directed_atg_edges: set[tuple[int, int]] = set()

        for i in range(len(upsilon)):
            for j in range(i + 1, len(upsilon)):
                edge = PosetUtils.edge_label(upsilon[i], upsilon[j])
                if edge:
                    edge = list(edge)
                    directed_atg_edges.add((int(edge[0]), int(edge[1])))
                    directed_atg_edges.add((int(edge[1]), int(edge[0])))

        if verbose:
            print(f"ATG Edges (directed): {directed_atg_edges}\n")

        A_star = combinations(directed_atg_edges, k - 1)
        legs: list[LinearExtensions] = []
        for anchor_pairs in A_star:
            upsilon_A: set[LinearOrder] = set()
            for linear_order in upsilon:
                linear_order_follows_anchor_pairs = all(
                    [
                        PosetUtils.x_is_less_than_y_in_L(linear_order, a, b)
                        for a, b in anchor_pairs
                    ]
                )
                if linear_order_follows_anchor_pairs:
                    upsilon_A.add(linear_order)

            A_is_a_poset = False
            partial_order_A = None
            if upsilon_A:
                partial_order_A = PosetUtils.get_partial_order_of_convex(upsilon_A)
                A_is_a_poset = (
                    set(
                        PosetUtils.get_linear_extensions_from_relation(
                            partial_order_A, upsilon[0]
                        )
                    )
                    == upsilon_A
                )

            if verbose:
                print(f"anchors: {anchor_pairs}")
                print(f"upsilon_A: {upsilon_A}")
                if upsilon_A:
                    print(f"is_poset: {A_is_a_poset}")

            if A_is_a_poset:
                maximal_supercover_linear_extensions = PosetSolver.maximal_poset(
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

    @staticmethod
    def maximal_poset(
        upsilon: list[LinearOrder],
        anchor_pairs: list[AnchorPair],
        partial_order: PartialOrder,
        verbose=False,
    ) -> LinearExtensions:
        """Find a maximal poset which supercovers the poset bounded by the input anchor pairs

        Preconditions:
            anchor_pairs must be a subset of partial_order.
            The linear extensions of the poset (determined by partial_order) must be a subset of upsilon.

        Args:
            upsilon: A list of linear orders of equal length
            anchor_pairs: The anchor pairs denote the relations the input poset must satisfy. The anchor pairs essentially isolate/bound linear orders in upsilon.
            partial_order: The partial order of the input poset.
            verbose: Print information while the function executes. Defaults to False.

        Returns:
            LinearExtensions: The linear extensions of a maximal poset which supercovers the input poset.

        Notes:
            The resulting partial_order_as_set is computed but not returned.
        """

        if verbose:
            print("Input")
            print(f"upsilon:       {upsilon}")
            print(f"anchor_pairs:  {anchor_pairs}")
            print(f"partial_order: {partial_order}\n")

        upsilon_as_set: set[LinearOrder] = set(upsilon)
        partial_order_as_set: set[tuple[int, int]] = set(partial_order)

        Y_covered: set[LinearOrder] = set(
            PosetUtils.get_linear_extensions_from_relation(partial_order, upsilon[0])
        )
        Y_uncovered: set[LinearOrder] = upsilon_as_set - Y_covered
        hasse: HasseDiagram = PosetUtils.get_hasse_from_partial_order(
            partial_order, upsilon[0]
        )

        J_sets: list[set[tuple[int, int]]] = [
            set(
                product(
                    PosetUtils.ancestors(a, hasse) | {a},
                    PosetUtils.descendants(b, hasse) | {b},
                )
            )
            for a, b in anchor_pairs
        ]
        J_unioned: list[tuple[int, int]] = list(set.union(*J_sets))
        J_unioned.sort(
            key=lambda anchor_pair: PosetUtils.hasse_dist(hasse, *anchor_pair)
        )

        I = copy.deepcopy(J_unioned)
        if verbose:
            print(f"Anchor Pairs ranked by distance, I: {I}")

        current_pair: tuple[int, int] | None = I[0]
        pair_index: int = 0
        blacklist: set[tuple[int, int]] = set()
        while True:
            x, y = current_pair
            L_xy: set[LinearOrder] = {
                linear_order
                for linear_order in Y_covered
                if PosetUtils.x_is_covered_by_y_in_L(linear_order, x=x, y=y)
            }
            L_yx: set[LinearOrder] = {
                PosetUtils.swap_xy_in_L(linear_order, x, y) for linear_order in L_xy
            }
            L_yx: set[LinearOrder] = {
                linear_order for linear_order in L_yx if linear_order in Y_uncovered
            }

            if verbose:
                print(f"\ncurrent_pair: {x} {y}")
                print(f"Y_covered:   {Y_covered}")
                print(f"Y_uncovered: {Y_uncovered}")
                print(f"L_xy:           {L_xy}")
                print(f"L_yx:     {L_yx}")

            if len(L_xy) == len(L_yx) and len(L_xy) != 0:
                convex_of_L_prime: set[LinearOrder] = set(
                    PosetUtils.generate_convex(list(L_yx))
                )
                if convex_of_L_prime <= upsilon_as_set:
                    partial_order_as_set -= {(x, y)}
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

            prev_pair: tuple[int, int] = (x, y)

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
