"""
Test Overview

Public interface of a PosetVisualizer (✓ - for testing; ✗ - maybe not)
 - select_nodes                 ✓ function is useful
 - highlight_nodes              ✗ not useful on its own
 - select_and_highlight_nodes   ✓ function is useful
 - update_figure                ✗ used only by the select node methods
 - show_figure                  ✗ not used
 - get_figure_data              ✓ main purpose of the visualizer

Some notes regarding the purpose of the select-node functions
    There are three classes of vertices and edges: selected, highlighted, and others
    All vertices and edges start as "others"
    select_nodes will move some vertices (and their edges) to "selected" class/status
    highlight_nodes will move some vertices (and their edges) to "highlighted" class/status
    select_and_highlight_nodes does both
    Only then is get_figure called (see main.py)


Charateristics of Nodes and Edges according to Class
    +-------------------+-------------------+-------------------+
    |       Class       |      Vertex       |       Edge        |
    +-------------------+-------------------+-------------------+
    |     Selected      |   color="black"   |color=<swap_color> |
    |                   |      size=3       |      width=2      |
    |                   |     opacity=1     |     opacity=1     |
    +-------------------+-------------------+-------------------+
    |    Highlighted    |    color="red"    |    color="red"    |
    |                   |      size=6       |      width=5      |
    |                   |     opacity=1     |     opacity=1     |
    +-------------------+-------------------+-------------------+
    |      Others       |   color="black"   |color=<swap_color> |
    |                   |      size=3       |      width=2      |
    |                   |    opacity=0.1    |    opacity=0.1    |
    +-------------------+-------------------+-------------------+

    Observations after investigating the traces.
        Except for the variable color (<swap_color>), colors red and black can be verified as literals "red" and "black"
        Then other attributes can be check for their numerical value

New Test Proposal
Now, since it is clear we are operating with three render types, I suppose we should not test for the definition anymore.
(Notice that the ATG in the paper does not deal with highlighted edges, nor "other" nodes.)
Instead, we should simply test for the render types and hope that our representation still contains the ATG.
It should also be noted that there is no test for .get_figure_data as its reliability is guaranteed by all the tests.
1. test_errors_raised
2. test "default" output (i.e. without selection; permutahedron). effectively the same as .select_nodes(<all_nodes>)
    Call PosetVisualizer(n) for n = 3 and 4
    a. nodes (selected)
    b. edges (selected, does not exist)
3. test select_nodes
    Call PosetVisualizer(n) for n = 3 and 4, then call .select_nodes()
    a. nodes (selected, other)
    b. edges (selected, other, does not exist)
4. test select_and_highlight_nodes()
    Call PosetVisualizer(n) for n = 3 and 4, then call .select_and_highlight_nodes()
    a. nodes (selected, highlighted, other)
    b. edges (selected, highlighted, other, does not exist)
"""

import pytest

from app.posetvisualizer import PosetVisualizer, RenderType
from tests.testing_utils import FigureTester

from .upsilon_constants import TWOMAXIMAL

RENDER_TYPE_SPECS = PosetVisualizer.RENDER_TYPE_SPECS


def verify_edges_have_the_same_color(
    tester: FigureTester, edges: list[tuple[str, str]]
) -> None:
    """Verify all edges provided have the same color. Not applicable to lists containing highlighted edges.

    Equivalent to verifying that all edges have the same swap, i.e. same equivalence class
    """
    edge0 = edges[0]
    edge_data0 = tester.get_edge_data(*edge0)

    assert (
        edge_data0
    ), f"edge '{edge0}', while expected to exist, does not exist in figure data"

    color0 = edge_data0["line"]["color"]
    for edge in edges[1:]:
        edge_data = tester.get_edge_data(*edge)

        assert (
            edge_data
        ), f"edge '{edge}', while expected to exist, does not exist in figure data"

        color = edge_data["line"]["color"]

        assert (
            color == color0
        ), f"expected {{edge: {edge}, color: {color} }} to have the same color as {{edge0: {edge0}, color: {color0} }}"


def verify_edges_have_different_colors(
    tester: FigureTester, edge1: tuple[str, str], edge2: tuple[str, str]
) -> None:
    """Verify that TWO edges differ in color. Not applicable to highlighted edges"""
    edge_data1 = tester.get_edge_data(*edge1)
    edge_data2 = tester.get_edge_data(*edge2)

    assert (
        edge_data1
    ), f"edge '{edge1}', while expected to exist, does not exist in figure data"
    assert (
        edge_data2
    ), f"edge '{edge2}', while expected to exist, does not exist in figure data"

    color1 = edge_data1["line"]["color"]
    color2 = edge_data2["line"]["color"]

    assert (
        color1 != color2
    ), f"expected {{edge1: {edge1}, color: {color1} }} to have a different color than {{edge2: {edge2}, color: {color2} }}"


def verify_edges_do_not_exist(tester, edges) -> None:
    """Verify if all edges provided are NOT part of the atg

    Any two permutations with one unreachable by an adjacent swap from the other should not constitute an edge\\
    That is, an "edge" between such permutations should not be part of the atg

    This function is usually used to check if the "edge" adheres to the definition of atg's\\
    In the future, we should perhaps check for edges not found in the supercover,
        or simply create new functions
    """
    for node_text1, node_text2 in edges:
        edge_data = tester.get_edge_data(node_text1, node_text2)
        assert (
            edge_data is None
        ), f"edge '{(node_text1, node_text2)}', while expected to not exist, does exist in figure data"


def verify_render_type_of_node(
    tester: FigureTester, node_text: str, render_type: RenderType
) -> bool:
    """Verify that the node is rendered as render_type

    Args:
        tester: The object containing the traces
        node_text: The text of the node like '1234', a LinearOrder
        render_type: The expected render type of the node

    Returns:
        bool:
    """
    node_data = tester.get_node_data(node_text)
    assert (
        node_data
    ), f"node '{node_text}', while expected to exist, does not exist in figure data"

    render_type_color = RENDER_TYPE_SPECS["node"][render_type]["color"]
    render_type_size = RENDER_TYPE_SPECS["node"][render_type]["size"]
    render_type_opacity = RENDER_TYPE_SPECS["node"][render_type]["opacity"]
    color = node_data["marker"]["color"]
    size = node_data["marker"]["size"]
    opacity = node_data["opacity"]

    same_color = color == render_type_color
    same_size = size == render_type_size
    same_opacity = opacity == render_type_opacity
    return same_color and same_size and same_opacity


def verify_render_type_of_edge(
    tester: FigureTester, edge: tuple[str, str], render_type: RenderType
) -> bool:
    """Verify that the edge is rendered as render_type

    Args:
        tester: The object containing the traces
        edge: An edge described by the text of its nodes, e.g. tuple('123','213')
        render_type: The expected render type of the edge

    Returns:
        bool:
    """
    node_text1, node_text2 = edge
    edge_data = tester.get_edge_data(node_text1, node_text2)
    assert (
        edge_data
    ), f"edge '{(node_text1, node_text2)}', while expected to exist, does not exist in figure data"

    highlighted_color = RENDER_TYPE_SPECS["edge"]["highlighted"]["color"]
    render_type_width = RENDER_TYPE_SPECS["edge"][render_type]["width"]
    render_type_opacity = RENDER_TYPE_SPECS["edge"][render_type]["opacity"]
    color = edge_data["line"]["color"]
    width = edge_data["line"]["width"]
    opacity = edge_data["opacity"]

    color_is_ok = render_type != "highlighted" or color == highlighted_color
    same_width = width == render_type_width
    same_opacity = opacity == render_type_opacity
    return color_is_ok and same_width and same_opacity


def verify_render_type_of_nodes(
    tester: FigureTester, nodes: list[str], render_type: RenderType
) -> None:
    """Verify that the nodes are rendered as render_type"""
    for node_text in nodes:
        is_correctly_rendered = verify_render_type_of_node(
            tester, node_text, render_type
        )
        assert (
            is_correctly_rendered
        ), f'expected node "{node_text}" is rendered as "{render_type}", but it\'s not'


def verify_render_type_of_edges(
    tester: FigureTester, edges: list[tuple[str, str]], render_type: RenderType
) -> None:
    """Verify that the edges are rendered as render_type"""
    for edge in edges:
        is_correctly_rendered = verify_render_type_of_edge(tester, edge, render_type)
        assert (
            is_correctly_rendered
        ), f'expected edge "{edge}" is rendered as "{render_type}", but it\'s not'


def test_errors_raised():
    with pytest.raises(Exception, match="at least 2"):
        PosetVisualizer(1)

    with pytest.raises(Exception, match=f"at most {PosetVisualizer.MAX_SIZE}"):
        PosetVisualizer(PosetVisualizer.MAX_SIZE + 1)

    with pytest.raises(TypeError, match="must be an integer"):
        PosetVisualizer("4")


def test_default_behavior():
    # ============ Size 3 ============ #
    visualizer = PosetVisualizer(3)
    tester = FigureTester(visualizer.get_figure_data())

    # selected/highlighted nodes are part of the atg
    # for this case, there are no "highlighted", "other", and "does not exist" nodes to check
    selected_nodes = ["123", "132", "213", "231", "312", "321"]
    verify_render_type_of_nodes(tester, selected_nodes, render_type="selected")

    # selected/highlighted edges are part of the atg, other edges are "visual aids"
    # for this case, there are no "highlighted" and "other" edges to check
    selected_edges = [("123", "132"), ("213", "231"), ("312", "321")]
    some_edges_that_dont_exist = [
        ("123", "312"),
        ("123", "321"),
        ("123", "231"),
        ("312", "213"),
    ]
    verify_render_type_of_edges(tester, selected_edges, render_type="selected")
    verify_edges_do_not_exist(tester, some_edges_that_dont_exist)

    # edges are colored according to swap type except highlighted edges
    edge_12 = [("123", "213"), ("312", "321")]
    edge_23 = [("123", "132"), ("231", "321")]
    diff_swap = [("123", "132"), ("123", "213")]
    verify_edges_have_the_same_color(tester, edge_23)
    verify_edges_have_the_same_color(tester, edge_12)
    verify_edges_have_different_colors(tester, *diff_swap)

    # ============ Size 4 ============ #
    visualizer = PosetVisualizer(4)
    tester = FigureTester(visualizer.get_figure_data())

    # selected/highlighted nodes are part of the atg
    # for this case, there are no "highlighted", "other", and "does not exist" nodes to check
    some_selected_nodes = ["1243", "1432", "2134", "2431", "4312", "3214"]
    verify_render_type_of_nodes(tester, some_selected_nodes, render_type="selected")

    # selected/highlighted edges are part of the atg, other edges are "visual aids"
    # for this case, there are no "highlighted" and "other" edges to check
    some_selected_edges = [("1423", "1432"), ("2134", "2143"), ("4312", "4321")]
    some_edges_that_dont_exist = [
        ("1234", "3124"),
        ("1423", "3421"),
        ("1243", "2341"),
        ("4312", "4213"),
    ]
    verify_render_type_of_edges(tester, some_selected_edges, render_type="selected")
    verify_edges_do_not_exist(tester, some_edges_that_dont_exist)

    # edges are colored according to swap type except highlighted edges
    edge_14 = [("2143", "2413"), ("3214", "3241"), ("1423", "4123")]
    edge_24 = [("1243", "1423"), ("2413", "4213"), ("1324", "1342")]
    diff_swap = [("1243", "1423"), ("1423", "4123")]
    verify_edges_have_the_same_color(tester, edge_14)
    verify_edges_have_the_same_color(tester, edge_24)
    verify_edges_have_different_colors(tester, *diff_swap)


def test_select_nodes():
    # ============ Size 3 ============ #
    visualizer = PosetVisualizer(3)
    selected_nodes = ["123", "132", "312", "321"]
    visualizer.select_nodes(selected_nodes)
    tester = FigureTester(visualizer.get_figure_data())

    # selected/highlighted nodes are part of the atg
    # for this case, there are no "highlighted", and "does not exist" nodes to check
    selected_nodes = selected_nodes
    other_nodes = ["231", "213"]
    verify_render_type_of_nodes(tester, selected_nodes, render_type="selected")
    verify_render_type_of_nodes(tester, other_nodes, render_type="other")

    # selected edges are part of the atg, other edges are "visual aids"
    # for this case, there are no "highlighted" edges to check
    selected_edges = [("123", "132"), ("132", "312"), ("312", "321")]
    other_edges = [("321", "231"), ("231", "213"), ("213", "123")]
    some_edges_that_dont_exist = [
        ("123", "312"),
        ("123", "321"),
        ("123", "231"),
        ("312", "213"),
    ]
    verify_render_type_of_edges(tester, selected_edges, render_type="selected")
    verify_render_type_of_edges(tester, other_edges, render_type="other")
    verify_edges_do_not_exist(tester, some_edges_that_dont_exist)

    # edges are colored according to swap type except highlighted edges
    # in this case, no "selected" edges have the same color
    diff_swap1 = [("123", "132"), ("132", "312")]
    diff_swap2 = [("123", "132"), ("312", "321")]
    diff_swap3 = [("132", "312"), ("312", "321")]
    verify_edges_have_different_colors(tester, *diff_swap1)
    verify_edges_have_different_colors(tester, *diff_swap2)
    verify_edges_have_different_colors(tester, *diff_swap3)

    # ============ Size 4 ============ #
    visualizer = PosetVisualizer(4)
    selected_nodes = TWOMAXIMAL
    visualizer.select_nodes(selected_nodes)
    tester = FigureTester(visualizer.get_figure_data())

    # selected/highlighted nodes are part of the atg
    # for this case, there are no "highlighted" and "does not exist" nodes to check
    selected_nodes = selected_nodes
    some_other_nodes = ["4321", "4231", "2413"]
    verify_render_type_of_nodes(tester, selected_nodes, render_type="selected")
    verify_render_type_of_nodes(tester, some_other_nodes, render_type="other")

    # selected/highlighted edges are part of the atg, other edges are "visual aids"
    # for this case, there are no "highlighted" edges to check
    some_selected_edges = [("2134", "2143"), ("1234", "1324"), ("3142", "3412")]
    some_other_edges = [("4321", "4231"), ("2143", "2413")]
    some_edges_that_dont_exist = [("1243", "3142"), ("4123", "4321"), ("1234", "2314")]
    verify_render_type_of_edges(tester, some_selected_edges, render_type="selected")
    verify_render_type_of_edges(tester, some_other_edges, render_type="other")
    verify_edges_do_not_exist(tester, some_edges_that_dont_exist)

    # edges are colored according to swap type except highlighted edges
    edge_24 = [("3124", "3142"), ("1324", "1342"), ("1243", "1423")]
    edge_13 = [("3124", "1324"), ("3142", "1342")]
    edge_23 = [("1423", "1432"), ("1234", "1324")]
    diff_swap = [("2134", "2143"), ("1234", "2134")]
    verify_edges_have_the_same_color(tester, edge_24)
    verify_edges_have_the_same_color(tester, edge_13)
    verify_edges_have_the_same_color(tester, edge_23)
    verify_edges_have_different_colors(tester, *diff_swap)


def test_select_and_highlight_nodes():
    # ============ Size 3 ============ #
    visualizer = PosetVisualizer(3)
    selected_nodes = ["123", "132", "312", "321"]
    highlighted_nodes = ["123", "132", "312"]
    visualizer.select_and_highlight_nodes(selected_nodes, highlighted_nodes)
    tester = FigureTester(visualizer.get_figure_data())

    # selected/highlighted nodes are part of the atg
    # for this case, there are no "does not exist" nodes to check
    selected_nodes = ["321"]
    other_nodes = ["231", "213"]
    highlighted_nodes = highlighted_nodes
    verify_render_type_of_nodes(tester, selected_nodes, render_type="selected")
    verify_render_type_of_nodes(tester, other_nodes, render_type="other")
    verify_render_type_of_nodes(tester, highlighted_nodes, render_type="highlighted")

    # selected edges are part of the atg, other edges are "visual aids"
    selected_edges = [("312", "321")]
    other_edges = [("321", "231"), ("231", "213"), ("213", "123")]
    highlighted_edges = [("132", "312"), ("123", "132")]
    some_edges_that_dont_exist = [
        ("123", "312"),
        ("123", "321"),
        ("123", "231"),
        ("312", "213"),
    ]
    verify_render_type_of_edges(tester, selected_edges, render_type="selected")
    verify_render_type_of_edges(tester, other_edges, render_type="other")
    verify_render_type_of_edges(tester, highlighted_edges, render_type="highlighted")
    verify_edges_do_not_exist(tester, some_edges_that_dont_exist)

    # edges are colored according to swap type except highlighted edges
    # in this case, two out of three edges are highlighted, so nothing to test

    # ============ Size 4 ============ #
    visualizer = PosetVisualizer(4)
    selected_nodes = TWOMAXIMAL
    highlighted_nodes = ["4123", "1423", "1243", "1234"]
    visualizer.select_and_highlight_nodes(selected_nodes, highlighted_nodes)
    tester = FigureTester(visualizer.get_figure_data())

    # selected/highlighted nodes are part of the atg
    # for this case, there are no "does not exist" nodes to check
    selected_nodes = list(set(TWOMAXIMAL) - set(highlighted_nodes))
    some_other_nodes = ["4321", "4231", "2413"]
    highlighted_nodes = highlighted_nodes
    verify_render_type_of_nodes(tester, selected_nodes, render_type="selected")
    verify_render_type_of_nodes(tester, some_other_nodes, render_type="other")
    verify_render_type_of_nodes(tester, highlighted_nodes, render_type="highlighted")

    # selected/highlighted edges are part of the atg, other edges are "visual aids"
    some_selected_edges = [("2134", "2143"), ("1234", "1324"), ("3142", "3412")]
    some_other_edges = [("4321", "4231"), ("2143", "2413")]
    highlighted_edges = [("4123", "1423"), ("1423", "1243"), ("1243", "1234")]
    some_edges_that_dont_exist = [("1243", "3142"), ("4123", "4321"), ("1234", "2314")]
    verify_render_type_of_edges(tester, some_selected_edges, render_type="selected")
    verify_render_type_of_edges(tester, some_other_edges, render_type="other")
    verify_render_type_of_edges(tester, highlighted_edges, render_type="highlighted")
    verify_edges_do_not_exist(tester, some_edges_that_dont_exist)

    # edges are colored according to swap type except highlighted edges
    edge_24 = [("3124", "3142"), ("1324", "1342")]
    edge_13 = [("3124", "1324"), ("3142", "1342")]
    edge_23 = [("1423", "1432"), ("1234", "1324")]
    diff_swap = [("2134", "2143"), ("1234", "2134")]
    verify_edges_have_the_same_color(tester, edge_24)
    verify_edges_have_the_same_color(tester, edge_13)
    verify_edges_have_the_same_color(tester, edge_23)
    verify_edges_have_different_colors(tester, *diff_swap)


def test_hexsquare_as_selected_nodes():
    LINEAR_EXTENSIONS = ["1234", "1243", "1324", "1342", "1423", "1432", "4123", "4132"]
    visualizer = PosetVisualizer(4)
    selected_nodes = LINEAR_EXTENSIONS
    visualizer.select_nodes(selected_nodes)
    tester = FigureTester(visualizer.get_figure_data())

    # selected/highlighted nodes are part of the atg
    # for this case, there are no "does not exist" nodes to check
    some_other_nodes = ["4321", "4231", "2413"]
    verify_render_type_of_nodes(tester, selected_nodes, render_type="selected")
    verify_render_type_of_nodes(tester, some_other_nodes, render_type="other")

    # selected/highlighted edges are part of the atg, other edges are "visual aids"
    some_selected_edges = [("1234", "1243"), ("1324", "1342"), ("4123", "4132")]
    some_other_edges = [("4321", "4231"), ("2143", "2413")]
    some_edges_that_dont_exist = [("1432", "4123"), ("1234", "1342"), ("1342", "1243")]
    verify_render_type_of_edges(tester, some_selected_edges, render_type="selected")
    verify_render_type_of_edges(tester, some_other_edges, render_type="other")
    verify_edges_do_not_exist(tester, some_edges_that_dont_exist)

    # edges are colored according to swap type except highlighted edges
    ["1234", "1243", "1324", "1342", "1423", "1432", "4123", "4132"]
    edge_14 = [("1423", "4123"), ("1432", "4132")]
    edge_23 = [("1234", "1324"), ("1423", "1432"), ("4123", "4132")]
    edge_24 = [("1324", "1342"), ("1243", "1423")]
    edge_34 = [("1234", "1243"), ("1432", "1342")]
    diff_swap = [("1423", "4123"), ("1243", "1423")]
    verify_edges_have_the_same_color(tester, edge_14)
    verify_edges_have_the_same_color(tester, edge_23)
    verify_edges_have_the_same_color(tester, edge_24)
    verify_edges_have_the_same_color(tester, edge_34)
    verify_edges_have_different_colors(tester, *diff_swap)
