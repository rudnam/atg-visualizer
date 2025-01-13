from itertools import permutations, combinations
import networkx as nx
import os
import plotly.graph_objects as go
import colorsys


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


def create_and_draw_graph(sequence, selected_nodes=None, opacity_others=0.1):
    """
    Create and visualize the graph, with options to highlight specific nodes

    Parameters:
    sequence: str - The original sequence (e.g., '12345')
    selected_nodes: list - List of permutations to highlight (e.g., ['12345', '21345'])
    opacity_others: float - Opacity for non-selected nodes and edges (0.0 to 1.0)
    """
    # Generate all permutations
    permutations_list = list(permutations(sequence))
    perm_strings = ["".join(p) for p in permutations_list]

    # Create the full graph
    G = nx.Graph()
    G.add_nodes_from(perm_strings)

    # Generate colors for edges
    number_pairs = list(combinations(sequence, 2))
    num_colors_needed = len(number_pairs)
    colors = generate_distinct_colors(num_colors_needed)
    pair_to_color = dict(zip(number_pairs, colors))

    # Store edges by their swap type
    edges_by_swap = {pair: [] for pair in number_pairs}

    # Add edges and categorize them
    for i in range(len(perm_strings)):
        for j in range(i + 1, len(perm_strings)):
            swapped_nums = get_swapped_numbers(perm_strings[i], perm_strings[j])
            if swapped_nums:
                edges_by_swap[swapped_nums].append((perm_strings[i], perm_strings[j]))
                G.add_edge(perm_strings[i], perm_strings[j])

    # Create a 3D layout for the full graph
    node_pos = nx.spring_layout(G, dim=3)

    # Create edge traces for each type of swap
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
            # Check if this edge should be highlighted
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

        # Create trace for selected edges
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

        # Create trace for other edges with reduced opacity and no hover
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
                    hoverinfo="skip",  # Disable hover for faded edges
                    showlegend=False,
                )
            )

    # Create node traces
    selected_nodes_x = []
    selected_nodes_y = []
    selected_nodes_z = []
    selected_nodes_text = []
    other_nodes_x = []
    other_nodes_y = []
    other_nodes_z = []
    other_nodes_text = []

    for node in G.nodes():
        pos = node_pos[node]
        if selected_nodes is None or node in selected_nodes:
            selected_nodes_x.append(pos[0])
            selected_nodes_y.append(pos[1])
            selected_nodes_z.append(pos[2])
            selected_nodes_text.append(node)
        else:
            other_nodes_x.append(pos[0])
            other_nodes_y.append(pos[1])
            other_nodes_z.append(pos[2])
            other_nodes_text.append(node)

    # Create trace for selected nodes
    if selected_nodes_x:
        node_trace_selected = go.Scatter3d(
            x=selected_nodes_x,
            y=selected_nodes_y,
            z=selected_nodes_z,
            mode="markers+text",
            marker=dict(size=5, color="black"),
            text=selected_nodes_text,
            textposition="top center",
            hoverinfo="text",
            name="Selected Permutations",
        )
        edge_traces.append(node_trace_selected)

    # Create trace for other nodes with reduced opacity and no hover
    if other_nodes_x:
        node_trace_others = go.Scatter3d(
            x=other_nodes_x,
            y=other_nodes_y,
            z=other_nodes_z,
            mode="markers+text",
            marker=dict(size=5, color="black"),
            text=other_nodes_text,
            textposition="top center",
            opacity=opacity_others,
            hoverinfo="skip",  # Disable hover for faded nodes
            name="Other Permutations",
            showlegend=False,
        )
        edge_traces.append(node_trace_others)

    # Set up the layout
    layout = go.Layout(
        scene=dict(
            xaxis=dict(title="X-axis"),
            yaxis=dict(title="Y-axis"),
            zaxis=dict(title="Z-axis"),
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        showlegend=True,
    )

    # Create and show the figure
    fig = go.Figure(data=edge_traces, layout=layout)
    html_file = os.path.join("static", "graph.html")
    fig.write_html(html_file)

    return html_file
