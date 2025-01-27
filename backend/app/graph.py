from itertools import permutations, combinations
import networkx as nx
import numpy as np
import pytest
import plotly.graph_objects as go


MAX_SIZE = 8


class PosetSolver:
    def __init__(self, size: int):
        if not type(size) is int:
            raise TypeError("Invalid size. Size must be an integer.")
        if size < 2 or size > MAX_SIZE:
            raise Exception(
                f"Invalid size. Size must have a value of at least 2 and at most {MAX_SIZE}"
            )

        sequence = "".join([str(x) for x in range(1, size + 1)])
        perm_strings = ["".join(p) for p in list(permutations(sequence))]

        self.__graph = nx.Graph()
        self.__graph.add_nodes_from(perm_strings)

        for i in range(len(perm_strings)):
            for j in range(i + 1, len(perm_strings)):
                if self._is_adjacent_swap(perm_strings[i], perm_strings[j]):
                    self.__graph.add_edge(perm_strings[i], perm_strings[j])

        self.__set_up_3d()

    def _is_adjacent_swap(self, p1: str, p2: str):
        if len(p1) != len(p2):
            raise Exception("Pair is not of the same length.")

        if p1 == p2:
            return False

        for i in range(len(p1) - 1):
            swapped = list(p1)
            swapped[i], swapped[i + 1] = swapped[i + 1], swapped[i]
            swapped = "".join(swapped)

            if swapped == p2:
                return True

        return False

    def __set_up_3d(self):
        pos = nx.spring_layout(self.__graph, dim=3)

        node_x = [pos[node][0] for node in self.__graph.nodes()]
        node_y = [pos[node][1] for node in self.__graph.nodes()]
        node_z = [pos[node][2] for node in self.__graph.nodes()]

        edge_x, edge_y, edge_z = [], [], []
        for edge in self.__graph.edges():
            x0, y0, z0 = pos[edge[0]]
            x1, y1, z1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            edge_z.extend([z0, z1, None])

        nodes_trace = go.Scatter3d(
            x=node_x,
            y=node_y,
            z=node_z,
            mode="markers",
            marker=dict(size=3, color="maroon", opacity=0.8),
            text=[node for node in self.__graph.nodes()],
            hoverinfo="text",
        )

        edges_trace = go.Scatter3d(
            x=edge_x,
            y=edge_y,
            z=edge_z,
            mode="lines",
            line=dict(color="gray", width=1),
            hoverinfo="none",
        )

        layout = go.Layout(
            scene=dict(
                xaxis_visible=False,
                yaxis_visible=False,
                zaxis_visible=False,
                bgcolor="rgba(0, 0, 0, 0)",
            ),
            margin=dict(l=0, r=0, b=0, t=0),
        )
        self.__fig_data = [edges_trace, nodes_trace]
        self.__fig_layout = layout

        self.__fig = go.Figure(data=[edges_trace, nodes_trace], layout=layout)

    def show_figure(self):
        self.__fig.show()

    def get_figure_data(self):
        return {"data": self.__fig_data, "layout": self.__fig_layout}


def testPosetSolver():
    with pytest.raises(Exception, match="at least 2"):
        PosetSolver(1)

    with pytest.raises(Exception, match=f"at most {MAX_SIZE}"):
        PosetSolver(MAX_SIZE + 1)

    with pytest.raises(TypeError, match="must be an integer"):
        PosetSolver("4")  # type: ignore

    p = PosetSolver(4)
    assert p._is_adjacent_swap("1234", "1324") == True
    assert p._is_adjacent_swap("1234", "3214") == False
    assert p._is_adjacent_swap("1234", "2134") == True

    p.show_figure()
