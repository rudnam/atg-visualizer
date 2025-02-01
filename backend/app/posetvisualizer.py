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
        self.selected_nodes = []
        self.highlighted_nodes = []

        self._set_up_graph()
        self._pos = nx.spring_layout(self._graph, dim=3, seed=42)
        self._edge_trace = self._compute_edge_traces()
        self._node_trace = self._compute_node_traces()
        self._fig_layout = self._make_fig_layout()

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

    def _compute_edge_traces(self):
        edge_traces = []
        for number_pair, edges in self._edges_by_swap.items():
            highlighted_edges = []
            selected_edges = []
            other_edges = []

            for edge in edges:
                p1, p2 = edge
                is_highlighted = (
                    p1 in self.highlighted_nodes and p2 in self.highlighted_nodes
                )
                is_selected = (
                    not is_highlighted
                    and (p1 in self.selected_nodes or p1 in self.highlighted_nodes)
                    and (p2 in self.selected_nodes or p2 in self.highlighted_nodes)
                )
                if is_highlighted:
                    highlighted_edges.append(edge)
                elif is_selected:
                    selected_edges.append(edge)
                else:
                    other_edges.append(edge)

            if highlighted_edges:
                trace = self._make_edge_trace(
                    highlighted_edges,
                    render_type="highlighted",
                    number_pair=number_pair,
                )
                edge_traces.append(trace)
            if selected_edges:
                trace = self._make_edge_trace(
                    selected_edges, render_type="selected", number_pair=number_pair
                )
                edge_traces.append(trace)
            if other_edges:
                trace = self._make_edge_trace(
                    other_edges, render_type="other", number_pair=number_pair
                )
                edge_traces.append(trace)

        return edge_traces

    def _make_edge_trace(self, edges, render_type="selected", number_pair=("1", "2")):
        selected_edges_x = []
        selected_edges_y = []
        selected_edges_z = []

        for edge in edges:
            p1, p2 = edge
            x_coords = [self._pos[p1][0], self._pos[p2][0], None]
            y_coords = [self._pos[p1][1], self._pos[p2][1], None]
            z_coords = [self._pos[p1][2], self._pos[p2][2], None]
            selected_edges_x.extend(x_coords)
            selected_edges_y.extend(y_coords)
            selected_edges_z.extend(z_coords)

        # set trace options according to render type
        line_dict = (
            dict(color="red", width=5, dash="solid")
            if render_type == "highlighted"
            else dict(color=self._pair_to_color[number_pair], width=2)
        )
        trace_opacity = 0.1 if render_type == "other" else 1
        trace_show_legend = render_type == "selected"

        return go.Scatter3d(
            x=selected_edges_x,
            y=selected_edges_y,
            z=selected_edges_z,
            mode="lines",
            line=line_dict,
            opacity=trace_opacity,
            name=f"Swap {number_pair[0]}-{number_pair[1]}",
            hoverinfo="skip",
            showlegend=trace_show_legend,
        )

    def _compute_node_traces(self):
        def node_is_other(node):
            return (
                not self._all_perms_are_selected()
                and node not in self.selected_nodes
                and node not in self.highlighted_nodes
            )

        selected_nodes = [
            node for node in self.selected_nodes if node not in self.highlighted_nodes
        ]
        other_nodes = [node for node in self._graph.nodes() if node_is_other(node)]

        node_traces = []
        if self.highlighted_nodes:
            node_traces.append(
                self._make_node_trace(self.highlighted_nodes, render_type="highlighted")
            )
        if selected_nodes:
            node_traces.append(
                self._make_node_trace(selected_nodes, render_type="selected")
            )
        if other_nodes:
            node_traces.append(self._make_node_trace(other_nodes, render_type="other"))
        return node_traces

    def _make_node_trace(self, nodes, render_type="selected"):
        # set trace options according to render type
        marker_dict = (
            dict(size=6, color="red")
            if render_type == "highlighted"
            else dict(size=3, color="black")
        )
        trace_opacity = 0.1 if render_type == "other" else 1
        trace_show_legend = render_type == "selected"

        selected_nodes_x = []
        selected_nodes_y = []
        selected_nodes_z = []
        selected_nodes_text = []

        for node in nodes:
            pos = self._pos[node]
            selected_nodes_x.append(pos[0])
            selected_nodes_y.append(pos[1])
            selected_nodes_z.append(pos[2])
            selected_nodes_text.append(node)

        return go.Scatter3d(
            x=selected_nodes_x,
            y=selected_nodes_y,
            z=selected_nodes_z,
            mode="markers+text",
            marker=marker_dict,
            text=selected_nodes_text,
            textposition="top center",
            opacity=trace_opacity,
            hoverinfo="skip",
            name="Permutations",
            showlegend=trace_show_legend,
        )

    def _make_fig_layout(self):
        return go.Layout(
            scene=dict(
                xaxis_visible=False,
                yaxis_visible=False,
                zaxis_visible=False,
                bgcolor="rgba(0, 0, 0, 0)",
            ),
            margin=dict(l=0, r=0, b=0, t=0),
        )

    def _all_perms_are_selected(self):
        return len(self.selected_nodes) == 0

    def select_nodes(self, select_nodes: List[str]):
        """Selects specified nodes"""
        self.selected_nodes = select_nodes
        self._node_trace = self._compute_node_traces()
        self._edge_trace = self._compute_edge_traces()
        self.update_figure()

    def highlight_nodes(self, select_nodes: List[str]):
        """Highlights specified nodes"""
        self.highlighted_nodes = select_nodes
        self._node_trace = self._compute_node_traces()
        self._edge_trace = self._compute_edge_traces()
        self.update_figure()

    def select_and_highlight_nodes(
        self, select_nodes: List[str], highlight_nodes: List[str]
    ):
        self.highlighted_nodes = highlight_nodes
        self.selected_nodes = select_nodes
        self._node_trace = self._compute_node_traces()
        self._edge_trace = self._compute_edge_traces()
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
