from itertools import combinations, chain
import networkx as nx
from typing import List, Tuple

from app.classes import LinearOrder


class PosetUtils:
    @staticmethod
    def get_linear_extensions(cover_relation):
        G = nx.DiGraph()
        for a, b in cover_relation:
            G.add_edge(a, b)
        sortings = list(nx.all_topological_sorts(G))
        return sorted(["".join(map(str, sorting)) for sorting in sortings])

    @staticmethod
    def verify(P, Y):
        return sorted(P) == sorted(Y)

    @staticmethod
    def verify_group(Group_P, Y):
        covered = []
        for P in Group_P:
            covered += PosetUtils.get_linear_extensions(P)
        return sorted(covered) == sorted(Y)

    @staticmethod
    def find_anchors(G):
        anchors = list(set(anchor[2]["label"] for anchor in G.edges.data()))
        anchors += ["".join(reversed(anchor)) for anchor in anchors]
        for i in range(len(anchors)):
            anchors[i] = (int(anchors[i][0]), int(anchors[i][3]))
        return anchors

    @staticmethod
    def no_dupe(anchors):
        N = len(anchors)
        for i in range(N - 1):
            for j in range(i + 1, N):
                if "".join(str(num) for num in anchors[i]) == "".join(
                    reversed("".join(str(num) for num in anchors[j]))
                ):
                    return False
        return True

    @staticmethod
    def group_anchors(anchors, k):
        return [
            combi for combi in combinations(anchors, k - 1) if PosetUtils.no_dupe(combi)
        ]

    @staticmethod
    def covers_upsilon(linear_orders, Upsilon):
        return set(Upsilon).issubset(set(linear_orders))

    @staticmethod
    def check_swap(str1, str2):
        for i in range(len(str1) - 1):
            if str1[i] == str2[i + 1] and str1[i + 1] == str2[i]:
                if str1[0:i] + str1[i + 2 :] != str2[0:i] + str2[i + 2 :]:
                    return None
                return f"{str(min(int(str1[i]), int(str2[i])))}, {str(max(int(str1[i]), int(str2[i])))}"
        return None

    @staticmethod
    def generatePoset(linear_orders: List[str]) -> List[Tuple[int, int]]:
        def parse_order(order_str: str) -> List[int]:
            return [int(char) for char in order_str]

        first_order = parse_order(linear_orders[0])
        initial_linear_order = LinearOrder(first_order)
        all_relations = set(initial_linear_order.relations)  # type: ignore

        for order_str in linear_orders[1:]:
            sequence = parse_order(order_str)
            linear_order = LinearOrder(sequence)
            all_relations.intersection_update(linear_order.relations)  # type: ignore

        sorted_relations = sorted(all_relations)
        return sorted_relations

    @staticmethod
    def linearOrdersToGraph(linear_orders: List[str]) -> nx.Graph:
        G = nx.Graph()
        N = len(linear_orders)
        for i in range(N):
            G.add_node(linear_orders[i])
            for j in range(i + 1, N):
                adjacent = PosetUtils.check_swap(linear_orders[i], linear_orders[j])
                if adjacent:
                    G.add_edge(
                        linear_orders[i],
                        linear_orders[j],
                        label=adjacent,
                        color="k",
                    )

        return G


class PosetCover:
    def __init__(self, upsilon, k):
        self.upsilon = upsilon
        self.k = int(k)
        self.G = PosetUtils.linearOrdersToGraph(upsilon)

    def find_covering_poset(self, Pstar, Upsilon):
        def covers_upsilon(linear_orders, Upsilon):
            for order in linear_orders:
                if any(ups in order for ups in Upsilon):
                    return True
            return False

        Pfinal = []
        LOfinal = []

        for P in Pstar:
            linear_order = PosetUtils.get_linear_extensions(P)

            covered_orders = []
            for order in Upsilon:
                if any(part in order for part in linear_order):
                    covered_orders.append(order)

            LOfinal.append(covered_orders)

            if covers_upsilon(linear_order, Upsilon):
                Pfinal.append(P)

        if not Pfinal:
            return None

        return Pfinal, LOfinal

    def maximalPoset(self, upsilon, P_A, A):
        G = nx.Graph()
        N = len(upsilon)

        for i in range(N):
            G.add_node(upsilon[i])
            for j in range(i + 1, N):
                adjacent = PosetUtils.check_swap(upsilon[i], upsilon[j])
                if adjacent:
                    G.add_edge(upsilon[i], upsilon[j], label=adjacent, color="k")

        Y_cov = PosetUtils.get_linear_extensions(P_A)

        Y_uncov = [u for u in upsilon if u not in Y_cov]

        Neighbors = {n: list(G.neighbors(n)) for n in G.nodes()}

        blacklist = []
        while 1:
            tempMirrors = []
            tempNodes = []
            for linear_ext in Y_cov:
                neighbors = Neighbors.get(linear_ext, [])
                for neighbor in neighbors:
                    if neighbor not in Y_cov and neighbor not in blacklist:
                        swap = PosetUtils.check_swap(linear_ext, neighbor)
                        if swap:
                            tempMirrors.append(
                                (tuple(map(int, swap.split(", "))), [neighbor])
                            )
                            tempNodes.append(neighbor)

            if len(tempNodes) == 0:
                break

            P_tempnodes = PosetUtils.generatePoset(tempNodes)
            LE_tempnodes = PosetUtils.get_linear_extensions(P_tempnodes)

            temp_cov = []
            for i in LE_tempnodes:
                if i in upsilon:
                    temp_cov.append(i)

            if sorted(
                PosetUtils.get_linear_extensions(
                    PosetUtils.generatePoset(list(set(Y_cov).union(set(temp_cov))))
                )
            ) == sorted(list(set(Y_cov).union(set(temp_cov)))):
                Y_cov = list(set(Y_cov).union(set(temp_cov)))

            else:
                for i in temp_cov:
                    if sorted(
                        PosetUtils.get_linear_extensions(
                            PosetUtils.generatePoset(Y_cov + [i])
                        )
                    ) == sorted(Y_cov + [i]):
                        Y_cov.append(i)

                    else:
                        blacklist.append(i)

        P_i = PosetUtils.generatePoset(Y_cov)

        return P_i

    def exact_k_poset_cover(self):
        anchors = PosetUtils.find_anchors(self.G)
        for i in range(1, self.k + 1):
            grouped_anchors = PosetUtils.group_anchors(anchors, self.k)
            Pstar_total = []
            for A in grouped_anchors:
                Upsilon_A = []
                for sequence in self.upsilon:
                    satisfies = True
                    for anchor in A:
                        a, b = str(anchor[0]), str(anchor[1])
                        if a in sequence and b in sequence:
                            if sequence.index(a) > sequence.index(b):
                                satisfies = False
                                break
                        else:
                            satisfies = False
                            break
                    if satisfies:
                        Upsilon_A.append(sequence)
                if Upsilon_A:
                    P_A = PosetUtils.generatePoset(Upsilon_A)
                    if P_A:
                        P_i = self.maximalPoset(self.upsilon, P_A, A)
                        Pstar_total.append(P_i)

            result = self.find_covering_poset(Pstar_total, self.upsilon)
            if result:
                P, L = result
                for q in range(len(L) - i):
                    if sorted(set(chain.from_iterable(L[q : q + i]))) == sorted(
                        self.upsilon
                    ):
                        Pfinal = P[q : q + i]
                        LOfinal = L[q : q + i]
                        return Pfinal, LOfinal
        return None
