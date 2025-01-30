INVALID = -1
Sequence = list[int]
Vertices = list[int]
Relations = list[tuple[(int, int)]]
LinearOrders = list[list[int]]


class Poset:

    def __init__(self, size: int, relations: Relations, isNull=False):
        self.vertices = None if isNull else [i for i in range(1, size + 1)]
        self.relations = None if isNull else sorted(relations)

    def isEmpty(self, keyword="both"):
        if keyword in ["both", "vertices"] and self.vertices == None:
            return True
        if keyword in ["both", "relations"] and self.relations == None:
            return True

        return False

    def isEqual(self, poset: "Poset") -> bool:
        if (
            (not self.isEmpty())
            and max(self.vertices) == max(poset.vertices)  # type: ignore
            and sorted(self.relations) == sorted(poset.relations)  # type: ignore
        ):
            return True

        return False

    def isIn(self, posets: list["Poset"]) -> bool:
        for poset in posets:
            if self.isEqual(poset):
                return True

        return False

    def subtract(self, poset: "Poset") -> Relations:
        relations = []
        for relation in self.relations:  # type: ignore
            if relation not in poset.relations:  # type: ignore
                relations.append(relation)

        return relations

    def generateLinearExtensions(self) -> list[LinearOrders]:
        graph = Graph(self.relations, len(self.vertices), [])  # type: ignore
        graph.getAllTopologicalOrders()

        return graph.listofLO


class LinearOrder(Poset):

    def __init__(self, sequence: Sequence):
        self.sequence = sequence
        super().__init__(len(sequence), self._getRelations(sequence))

    def _getRelations(self, sequence: Sequence) -> Relations:
        relations = []
        for i in range(0, len(sequence) - 1):
            for j in range(i + 1, len(sequence)):
                relations.append((sequence[i], sequence[j]))

        return relations
