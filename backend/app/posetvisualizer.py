from typing import TypedDict, Literal
from itertools import permutations, combinations, chain
import networkx as nx
import plotly.graph_objects as go
import seaborn as sns
import numpy as np

from numpy.typing import NDArray
from app.classes import *
from app.posetutils import PosetUtils


class NodeRenderSpecification(TypedDict):
    color: str
    size: int
    opacity: float


class EdgeRenderSpecification(TypedDict):
    color: str
    width: int
    opacity: float


class EdgeRenderSpecificationForSelectedOther(TypedDict):
    width: int
    opacity: float


class NodeRenderTypeSpecs(TypedDict):
    selected: NodeRenderSpecification
    highlighted: NodeRenderSpecification
    other: NodeRenderSpecification


class EdgeRenderTypeSpecs(TypedDict):
    selected: EdgeRenderSpecificationForSelectedOther
    highlighted: EdgeRenderSpecification
    other: EdgeRenderSpecificationForSelectedOther


class RenderTypeSpecs(TypedDict):
    node: NodeRenderTypeSpecs
    edge: EdgeRenderTypeSpecs


type RenderType = Literal["selected", "highlighted", "other"]


class PosetVisualizer:
    MAX_SIZE = 8

    RENDER_TYPE_SPECS: RenderTypeSpecs = {
        "node": {
            "selected": {"color": "black", "size": 3, "opacity": 1},
            "highlighted": {"color": "red", "size": 6, "opacity": 1},
            "other": {"color": "black", "size": 3, "opacity": 0.1},
        },
        "edge": {
            "selected": {"width": 3, "opacity": 1},
            "highlighted": {"color": "red", "width": 5, "opacity": 1},
            "other": {"width": 3, "opacity": 0.1},
        },
        # showlegend is also affected by render_type but not specified in this specs
    }

    def __init__(
        self,
        size: int,
        upsilon: list[LinearOrder] = [],
        # highlighted_poset: LinearExtensions = [],
        temp_permutahedron_embed=False,
        temp_include_supercover=False,
        temp_include_hexagonal=False,
        temp_one_hexagon_only=False,
        highlighted_poset: LinearExtensions = [],
    ):
        """Draw an Adjacent Transposition Graph optionally with highlighted portion

        Args:
            size: The length of a linear order. Convetionally indicated as 'n' in our main references.
            upsilon: The set of linear orders to draw. Defaults to [] which is interpreted as all possible linear orders of length 'size'.
            highlighted_poset: The set of linear extensions to highlight. Can be any subset of upsilon. Defaults to []; nothing to highlight.

        Raises:
            TypeError:
            ValueError:
        """

        print(
            f"Im called with these options: {temp_permutahedron_embed} {temp_include_supercover} {temp_include_hexagonal} {temp_one_hexagon_only}"
        )

        if not isinstance(size, int):
            raise TypeError("Invalid size. Size must be an integer.")
        if size < 2 or size > self.MAX_SIZE:
            raise ValueError(
                f"Invalid size. Size must have a value of at least 2 and at most {self.MAX_SIZE}."
            )

        # Section: Get support nodes according to upsilon
        self._support_nodes = self._get_support_nodes(
            upsilon,
            include_supercover=temp_include_supercover,
            include_hexagonal=temp_include_hexagonal,
            one_hexagon_only=temp_one_hexagon_only,
        )

        # Section: Encode graph information
        if upsilon:
            self.selected_nodes: list[LinearOrder] = upsilon
        else:
            sequence: str = "".join(map(str, range(1, size + 1)))
            perm_strings = ["".join(p) for p in permutations(sequence)]
            self.selected_nodes: list[LinearOrder] = perm_strings

        graph_plus_info = self._get_graph_and_additional_info()
        self._graph: nx.Graph = graph_plus_info["graph"]
        # for the next properties, str means '1', '2', '3', etc. except for the values of _pair_to_color which are of course colors
        self._edges_by_swap: dict[
            tuple[str, str], list[tuple[LinearOrder, LinearOrder]]
        ] = graph_plus_info["edges_by_swap"]
        self._pair_to_color: dict[tuple[str, str], str] = graph_plus_info[
            "pair_to_color"
        ]

        # Section: Compute coordinates
        self._pos: dict[LinearOrder, NDArray[np.float64]] = nx.spring_layout(
            self._graph, dim=3, seed=42, iterations=70
        )

        # Section: Drawing traces
        self.highlighted_nodes: LinearExtensions = highlighted_poset
        self._edge_trace: list[go.Scatter3d] = self._compute_edge_traces()
        self._node_trace: list[go.Scatter3d] = self._compute_node_traces()
        self._fig_layout: go.Layout = self._make_fig_layout()

        self._fig: go.Figure
        self.update_figure()

    @staticmethod
    def _get_swapped_numbers(p1: str, p2: str) -> tuple[str, str] | None:
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
        """Create a n-color color pallete"""
        palette = sns.color_palette("hls", n_colors).as_hex()
        return palette

    def _get_graph_and_additional_info(self):
        """Sets up graph and swap types"""
        perm_strings = self.selected_nodes
        graph = nx.Graph()
        graph.add_nodes_from(perm_strings)
        edges_by_swap: dict[tuple[str, str], list[tuple[LinearOrder, LinearOrder]]] = (
            dict()
        )

        perms_plus_support = perm_strings + list(self._support_nodes)
        for i in range(len(perms_plus_support)):
            for j in range(i + 1, len(perms_plus_support)):
                perm1 = perms_plus_support[i]
                perm2 = perms_plus_support[j]
                swapped_nums = self._get_swapped_numbers(perm1, perm2)

                if swapped_nums:
                    graph.add_edge(perm1, perm2)

                    # update edges by swap
                    if (
                        not self._support_nodes
                        or perm1 not in self._support_nodes
                        and perm2 not in self._support_nodes
                    ):
                        edge = (perm1, perm2)
                        if swapped_nums in edges_by_swap.keys():
                            edges_by_swap[swapped_nums].append(edge)
                        else:
                            edges_by_swap[swapped_nums] = [edge]

        number_pairs = edges_by_swap.keys()
        colors = self._generate_colors(len(number_pairs))
        pair_to_color = dict(zip(number_pairs, colors))

        return {
            "graph": graph,
            "edges_by_swap": edges_by_swap,
            "pair_to_color": pair_to_color,
        }

    def _get_support_nodes(
        self,
        upsilon: list[LinearOrder],
        include_supercover=False,
        include_hexagonal=False,
        one_hexagon_only=False,
    ) -> list[LinearOrder]:
        if not upsilon:
            print("Warn: Upsilon is empty.")
            return []
        support_nodes: set[LinearOrder] = set()
        if include_supercover:
            support_nodes |= set(PosetUtils.generate_convex(upsilon))

        if include_hexagonal:
            perm_strings = list(set.union(support_nodes, set(upsilon)))

            for i in range(len(perm_strings)):
                for j in range(i + 1, len(perm_strings)):
                    swapped_nums = self._get_swapped_numbers(
                        perm_strings[i], perm_strings[j]
                    )
                    if swapped_nums:
                        edge = (perm_strings[i], perm_strings[j])
                        two_hexagons = self._get_hexagonal_support_nodes(
                            edge, swapped_nums, one_hexagon_only
                        )
                        support_nodes |= set(two_hexagons)

        support_nodes -= set(upsilon)
        return sorted(support_nodes)

    @staticmethod
    def _get_hexagonal_support_nodes(
        edge: tuple[LinearOrder, LinearOrder],
        swapped_nums: tuple[str, str],
        one_hexagon_only=False,
    ) -> list[LinearOrder]:
        """Get the linear orders of the two hexagons containing the edge

        Args:
            edge: A pair of linear orders connected by an edge in the ATG
            swapped_nums: The swapped numbers in the edge. Required

        Returns:
            list[LinearOrder]: (list[str]) the linear orders of the hexagons
        """
        edge0: LinearOrder = edge[0]
        smaller_idx = edge0.index(swapped_nums[0])
        bigger_idx = edge0.index(swapped_nums[1])

        if smaller_idx > bigger_idx:
            temp = smaller_idx
            smaller_idx = bigger_idx
            bigger_idx = temp

        support_nodes: set[LinearOrder] = set()

        one_hex_done = False

        if smaller_idx > 0:
            # illustration. if edge0 = 23451 and smaller_idx is 2, then to_permute=345
            to_permute = edge0[smaller_idx - 1 : smaller_idx + 2]
            perms = permutations(to_permute)
            left_half = edge0[: smaller_idx - 1]
            right_half = edge0[smaller_idx + 2 :]
            hexagon = {f'{left_half}{"".join(perm)}{right_half}' for perm in perms}
            support_nodes |= hexagon
            if one_hexagon_only:
                one_hex_done = True

        if bigger_idx < len(edge0) - 1 and not one_hex_done:
            # continuing the illustration, bigger_idx should be 3, then to_permute=451
            to_permute = edge0[bigger_idx - 1 : bigger_idx + 2]
            perms = permutations(to_permute)
            left_half = edge0[: bigger_idx - 1]
            right_half = edge0[bigger_idx + 2 :]
            hexagon = {f'{left_half}{"".join(perm)}{right_half}' for perm in perms}
            support_nodes |= hexagon

        return list(support_nodes)

    def _compute_edge_traces(self) -> list[go.Scatter3d]:
        """Categorize edges and create the corresponding traces"""
        edge_traces: list[go.Scatter3d] = []
        for number_pair, edges in self._edges_by_swap.items():
            highlighted_edges: list[tuple[LinearOrder, LinearOrder]] = []
            selected_edges: list[tuple[LinearOrder, LinearOrder]] = []
            other_edges: list[tuple[LinearOrder, LinearOrder]] = []

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

    def _make_edge_trace(
        self,
        edges: list[tuple[LinearOrder, LinearOrder]],
        render_type: RenderType = "selected",
        number_pair: tuple[str, str] = ("1", "2"),
    ) -> go.Scatter3d:
        """Create an edge trace"""
        # set trace options according to render type
        edge_color_by_swap = self._pair_to_color[number_pair]
        edge_color_highlighted = self.RENDER_TYPE_SPECS["edge"]["highlighted"]["color"]
        edge_color = (
            edge_color_highlighted
            if render_type == "highlighted"
            else edge_color_by_swap
        )
        line_dict = dict(
            color=edge_color,
            width=self.RENDER_TYPE_SPECS["edge"][render_type]["width"],
        )
        trace_opacity = self.RENDER_TYPE_SPECS["edge"][render_type]["opacity"]
        trace_show_legend = render_type == "selected"

        selected_edges_x: list[np.float64 | None] = []
        selected_edges_y: list[np.float64 | None] = []
        selected_edges_z: list[np.float64 | None] = []

        for edge in edges:
            p1, p2 = edge
            x_coords = [self._pos[p1][0], self._pos[p2][0], None]
            y_coords = [self._pos[p1][1], self._pos[p2][1], None]
            z_coords = [self._pos[p1][2], self._pos[p2][2], None]
            selected_edges_x.extend(x_coords)
            selected_edges_y.extend(y_coords)
            selected_edges_z.extend(z_coords)

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

    def _compute_node_traces(self) -> list[go.Scatter3d]:
        """Categorize nodes and create the corresponding traces"""

        def node_is_other(node: LinearOrder) -> bool:
            return (
                node not in self.selected_nodes and node not in self.highlighted_nodes
            )

        selected_nodes: list[LinearOrder] = [
            node for node in self.selected_nodes if node not in self.highlighted_nodes
        ]
        other_nodes: list[LinearOrder] = [
            node for node in self._graph.nodes() if node_is_other(node)
        ]

        node_traces: list[go.Scatter3d] = []
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

    def _make_node_trace(
        self, nodes: list[LinearOrder], render_type: RenderType = "selected"
    ) -> go.Scatter3d:
        """Create a node trace"""
        # set trace options according to render type
        marker_dict = dict(
            color=self.RENDER_TYPE_SPECS["node"][render_type]["color"],
            size=self.RENDER_TYPE_SPECS["node"][render_type]["size"],
        )
        trace_opacity = self.RENDER_TYPE_SPECS["node"][render_type]["opacity"]
        trace_show_legend = render_type == "selected"

        selected_nodes_x: list[np.float64] = []
        selected_nodes_y: list[np.float64] = []
        selected_nodes_z: list[np.float64] = []
        selected_nodes_text: list[LinearOrder] = []

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

    def _make_fig_layout(self) -> go.Layout:
        """Create the figure layout"""
        return go.Layout(
            scene=dict(
                xaxis_visible=False,
                yaxis_visible=False,
                zaxis_visible=False,
                bgcolor="rgba(0, 0, 0, 0)",
            ),
            margin=dict(l=0, r=0, b=0, t=0),
            legend=dict(
                xanchor="right",
                yanchor="top",
                bgcolor="rgba(255, 255, 255, 0.3)",
            ),
        )

    def select_nodes(self, select_nodes: list[LinearOrder]) -> None:
        """Selects specified nodes"""
        self.selected_nodes = select_nodes
        self._node_trace = self._compute_node_traces()
        self._edge_trace = self._compute_edge_traces()
        self.update_figure()

    def highlight_nodes(self, select_nodes: list[LinearOrder]) -> None:
        """Highlights specified nodes"""
        self.highlighted_nodes = select_nodes
        self._node_trace = self._compute_node_traces()
        self._edge_trace = self._compute_edge_traces()
        self.update_figure()

    def select_and_highlight_nodes(
        self, select_nodes: list[LinearOrder], highlight_nodes: list[LinearOrder]
    ) -> None:
        self.highlighted_nodes = highlight_nodes
        self.selected_nodes = select_nodes
        self._node_trace = self._compute_node_traces()
        self._edge_trace = self._compute_edge_traces()
        self.update_figure()

    def update_figure(self) -> None:
        """Updates figure."""
        self._fig = go.Figure(
            data=[*self._edge_trace, *self._node_trace], layout=self._fig_layout
        )

    def show_figure(self) -> None:
        """Displays the current visualization."""
        self._fig.show()

    def get_figure_data(self) -> dict[str, list[go.Scatter3d] | go.Layout]:
        """Gets the figure data."""
        return {
            "data": [*self._edge_trace, *self._node_trace],
            "layout": self._fig_layout,
        }
