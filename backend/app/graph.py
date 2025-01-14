import networkx as nx
from itertools import permutations, combinations
import colorsys
import plotly.graph_objects as go


def generate_distinct_colors(n):
    """
    Generate n visually distinct colors using HSV color space
    """
    colors = []
    for i in range(n):
        hue = i / n
        rgb = colorsys.hsv_to_rgb(hue, 0.9, 0.9)
        color = "#{:02x}{:02x}{:02x}".format(
            int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
        )
        colors.append(color)
    return colors


def get_swapped_numbers(p1, p2):
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


def create_graph(
    sequence: str, selected_nodes: list | None = None, opacity_others: float = 0.1
):
    """
    Create and return the graph as a plotly JSON object.

    Parameters:
    sequence: str - The original sequence (e.g., '12345')
    selected_nodes: list - List of permutations to highlight (e.g., ['12345', '21345'])
    opacity_others: float - Opacity for non-selected nodes and edges (0.0 to 1.0)
    """
    permutations_list = list(permutations(sequence))
    perm_strings = ["".join(p) for p in permutations_list]

    G = nx.Graph()
    G.add_nodes_from(perm_strings)

    number_pairs = list(combinations(sequence, 2))
    num_colors_needed = len(number_pairs)
    colors = generate_distinct_colors(num_colors_needed)
    pair_to_color = dict(zip(number_pairs, colors))

    edges_by_swap = {pair: [] for pair in number_pairs}

    for i in range(len(perm_strings)):
        for j in range(i + 1, len(perm_strings)):
            swapped_nums = get_swapped_numbers(perm_strings[i], perm_strings[j])
            if swapped_nums:
                edges_by_swap[swapped_nums].append((perm_strings[i], perm_strings[j]))
                G.add_edge(perm_strings[i], perm_strings[j])

    node_pos = nx.spring_layout(G, dim=3, iterations=100)

    edge_traces = []
    for number_pair, edges in edges_by_swap.items():
        selected_edges_x = []
        selected_edges_y = []
        selected_edges_z = []
        other_edges_x = []
        other_edges_y = []
        other_edges_z = []

        for edge in edges:
            p1, p2 = edge
            is_selected = selected_nodes is None or (
                p1 in selected_nodes and p2 in selected_nodes
            )

            x_coords = [node_pos[p1][0], node_pos[p2][0], None]
            y_coords = [node_pos[p1][1], node_pos[p2][1], None]
            z_coords = [node_pos[p1][2], node_pos[p2][2], None]

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
                    line=dict(color=pair_to_color[number_pair], width=2),
                    name=f"Swap {number_pair[0]}-{number_pair[1]}",
                    hoverinfo="name",
                )
            )

        if other_edges_x:
            edge_traces.append(
                go.Scatter3d(
                    x=other_edges_x,
                    y=other_edges_y,
                    z=other_edges_z,
                    mode="lines",
                    line=dict(color=pair_to_color[number_pair], width=2),
                    opacity=opacity_others,
                    name=f"Swap {number_pair[0]}-{number_pair[1]} (other)",
                    hoverinfo="skip",
                    showlegend=False,
                )
            )

    layout = go.Layout(
        scene=dict(
            xaxis=dict(title="X-axis"),
            yaxis=dict(title="Y-axis"),
            zaxis=dict(title="Z-axis"),
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        showlegend=True,
    )
    return {"data": edge_traces, "layout": layout}
