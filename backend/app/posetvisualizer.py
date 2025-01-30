from itertools import permutations, combinations, chain
import networkx as nx
import plotly.graph_objects as go
from typing import List
import seaborn as sns


class PosetVisualizer:
    MAX_SIZE = 8

    def __init__(self, size: int):
        if not isinstance(size, int):
            raise TypeError("Invalid size. Size must be an integer.")
        if size < 2 or size > self.MAX_SIZE:
            raise ValueError(
                f"Invalid size. Size must have a value of at least 2 and at most {self.MAX_SIZE}."
            )

        self.size = size
        self.highlighted_nodes = []

        self._set_up_graph()

        self._pos = nx.spring_layout(self._graph, dim=3, seed=42)
        self._edge_trace = self._compute_edge_trace()
        self._node_positions = self._compute_node_positions()
        self._node_trace = self._compute_node_trace()
        self._fig_layout = go.Layout(
            scene=dict(
                xaxis_visible=False,
                yaxis_visible=False,
                zaxis_visible=False,
                bgcolor="rgba(0, 0, 0, 0)",
            ),
            margin=dict(l=0, r=0, b=0, t=0),
        )

        self.update_figure()

    @staticmethod
    def _get_swapped_numbers(p1: str, p2: str):
        """
        Returns the two numbers that were swapped between permutations,
        or None if not a valid adjacent transposition
        """
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
    def _generate_colors(n_colors: int):
        palette = sns.color_palette("hls", n_colors).as_hex()
        return palette

    def _set_up_graph(self):
        """Sets up graph and swap types"""
        sequence = "".join(map(str, range(1, self.size + 1)))
        number_pairs = list(combinations(sequence, 2))
        perm_strings = ["".join(p) for p in permutations(sequence)]
        self._graph = nx.Graph()
        self._graph.add_nodes_from(perm_strings)

        number_pairs = list(combinations(sequence, 2))
        colors = self._generate_colors(len(number_pairs))
        self._pair_to_color = dict(zip(number_pairs, colors))

        self._edges_by_swap = {pair: [] for pair in number_pairs}

        for i in range(len(perm_strings)):
            for j in range(i + 1, len(perm_strings)):
                swapped_nums = self._get_swapped_numbers(
                    perm_strings[i], perm_strings[j]
                )
                if swapped_nums:
                    self._edges_by_swap[swapped_nums].append(  # type: ignore
                        (perm_strings[i], perm_strings[j])
                    )
                    self._graph.add_edge(perm_strings[i], perm_strings[j])

    def _compute_edge_trace(self):
        """Computes edge traces."""
        edge_traces = []

        for number_pair, edges in self._edges_by_swap.items():
            selected_edges_x = []
            selected_edges_y = []
            selected_edges_z = []
            other_edges_x = []
            other_edges_y = []
            other_edges_z = []

            for edge in edges:
                p1, p2 = edge

                is_selected = len(self.highlighted_nodes) == 0 or (
                    p1 in self.highlighted_nodes and p2 in self.highlighted_nodes
                )

                x_coords = [self._pos[p1][0], self._pos[p2][0], None]
                y_coords = [self._pos[p1][1], self._pos[p2][1], None]
                z_coords = [self._pos[p1][2], self._pos[p2][2], None]

                if is_selected:
                    selected_edges_x.extend(x_coords)
                    selected_edges_y.extend(y_coords)
                    selected_edges_z.extend(z_coords)
                else:
                    other_edges_x.extend(x_coords)
                    other_edges_y.extend(y_coords)
                    other_edges_z.extend(z_coords)

            if selected_edges_x:
                edge_traces.append(
                    go.Scatter3d(
                        x=selected_edges_x,
                        y=selected_edges_y,
                        z=selected_edges_z,
                        mode="lines",
                        line=dict(color=self._pair_to_color[number_pair], width=2),
                        name=f"Swap {number_pair[0]}-{number_pair[1]}",
                        hoverinfo="skip",
                    )
                )

            if other_edges_x:
                edge_traces.append(
                    go.Scatter3d(
                        x=other_edges_x,
                        y=other_edges_y,
                        z=other_edges_z,
                        mode="lines",
                        line=dict(color=self._pair_to_color[number_pair], width=2),
                        opacity=0.1,
                        name=f"Swap {number_pair[0]}-{number_pair[1]} (other)",
                        hoverinfo="skip",
                        showlegend=False,
                    )
                )

        return edge_traces

    def _compute_node_positions(self):
        """Computes node positions."""
        node_x = [self._pos[node][0] for node in self._graph.nodes()]
        node_y = [self._pos[node][1] for node in self._graph.nodes()]
        node_z = [self._pos[node][2] for node in self._graph.nodes()]
        return node_x, node_y, node_z

    def _compute_node_trace(self):
        """Computes node traces"""

        node_traces = []

        selected_nodes_x = []
        selected_nodes_y = []
        selected_nodes_z = []
        selected_nodes_text = []
        other_nodes_x = []
        other_nodes_y = []
        other_nodes_z = []
        other_nodes_text = []

        for node in self._graph.nodes():
            pos = self._pos[node]
            if len(self.highlighted_nodes) == 0 or node in self.highlighted_nodes:
                selected_nodes_x.append(pos[0])
                selected_nodes_y.append(pos[1])
                selected_nodes_z.append(pos[2])
                selected_nodes_text.append(node)
            else:
                other_nodes_x.append(pos[0])
                other_nodes_y.append(pos[1])
                other_nodes_z.append(pos[2])
                other_nodes_text.append(node)

        node_x, node_y, node_z = self._node_positions

        if selected_nodes_x:
            node_trace_selected = go.Scatter3d(
                x=selected_nodes_x,
                y=selected_nodes_y,
                z=selected_nodes_z,
                mode="markers+text",
                marker=dict(size=3, color="black"),
                text=selected_nodes_text,
                textposition="top center",
                hoverinfo="skip",
                name="Permutations",
            )
            node_traces.append(node_trace_selected)

        if other_nodes_x:
            node_trace_others = go.Scatter3d(
                x=other_nodes_x,
                y=other_nodes_y,
                z=other_nodes_z,
                mode="markers+text",
                marker=dict(size=3, color="black"),
                text=other_nodes_text,
                textposition="top center",
                opacity=0.1,
                hoverinfo="skip",
                name="Other Permutations",
                showlegend=False,
            )
            node_traces.append(node_trace_others)

        return node_traces

    def highlight_nodes(self, highlight_nodes: List[str]):
        """Highlights specified nodes"""
        self.highlighted_nodes = highlight_nodes
        self._node_trace = self._compute_node_trace()
        self._edge_trace = self._compute_edge_trace()

        self.update_figure()

    def update_figure(self):
        """Updates figure."""
        self._fig = go.Figure(
            data=[*self._edge_trace, *self._node_trace], layout=self._fig_layout
        )

    def show_figure(self):
        """Displays the current visualization."""
        self._fig.show()

    def get_figure_data(self):
        """Gets the figure data."""
        return {
            "data": [*self._edge_trace, *self._node_trace],
            "layout": self._fig_layout,
        }
