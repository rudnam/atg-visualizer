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

Proposed Test Organization
1. test "default" output (i.e. without selection; permutahedron). effectively the same as .select_nodes(<all_nodes>)
    Call PosetVisualizer(n) for n = 3 to 5
    a. edges
    b. nodes
2. test select_nodes
    Call PosetVisualizer(n) for n = 3 and 4, then call .select_nodes()
    a. edges
    b. nodes
3. test select_and_highlight_nodes()
    Call PosetVisualizer(n) for n = 3 and 4, then call .select_and_highlight_nodes()
    a. edges
    b. nodes

New Test Proposal
Now, since it is clear we are operating with three render types, I suppose we should not test for the definition anymore.
(Notice that the ATG in the paper does not deal with highlighted edges, nor "other" nodes.)
Instead, we should simply test for the render types and hope that our representation still contains the ATG.
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


def _verify_egdes_have_the_same_color(
    tester: FigureTester, edges: list[tuple[str, str]]
) -> bool:
    """Verify edges provided all have the same color. Not applicable to lists containing highlighted edges.

    Equivalent to verifying that all edges have the same swap, i.e. same equivalence class
    """
    edge0 = edges[0]
    color0 = tester.get_edge_data(*edge0)["line"]["color"]
    for edge in edges[1:]:
        color = tester.get_edge_data(*edge)["line"]["color"]
        if color != color0:
            return False
    return True


def _verify_edges_do_not_exist(tester, edges) -> bool:
    """Verify if all edges provided are NOT part of the atg

    Edges which differ with more than one adjacent swap should not be part of the atg
    """
    for node_text1, node_text2 in edges:
        edge_data = tester.get_edge_data(node_text1, node_text2)
        if edge_data is not None:
            return False  # f"edge provided '{(node_text1, node_text2)}', while expected to not exist, does exist in figure data"
    return True


def _verify_render_type_of_nodes(
    tester: FigureTester, nodes: list[str], render_type: RenderType
) -> bool:
    render_type_color = RENDER_TYPE_SPECS["node"][render_type]["color"]
    render_type_size = RENDER_TYPE_SPECS["node"][render_type]["size"]
    render_type_opacity = RENDER_TYPE_SPECS["node"][render_type]["opacity"]
    for node_text in nodes:
        node_data = tester.get_node_data(node_text)
        assert (
            node_data
        ), f"node '{node_text}', while expected to exist, does not exist in figure data"
        color = node_data["marker"]["color"]
        size = node_data["marker"]["size"]
        opacity = node_data["opacity"]
        if not all(
            [
                color == render_type_color,
                size == render_type_size,
                opacity == render_type_opacity,
            ]
        ):
            return False
    return True


def _verify_render_type_of_edges(
    tester: FigureTester, edges: list[tuple[str, str]], render_type: RenderType
) -> bool:
    highlighted_color = RENDER_TYPE_SPECS["edge"]["highlighted"]["color"]
    render_type_width = RENDER_TYPE_SPECS["edge"][render_type]["width"]
    render_type_opacity = RENDER_TYPE_SPECS["edge"][render_type]["opacity"]
    for node_text1, node_text2 in edges:
        edge_data = tester.get_edge_data(node_text1, node_text2)
        assert (
            edge_data
        ), f"edge '{(node_text1, node_text2)}', while expected to exist, does not exist in figure data"
        color = edge_data["line"]["color"]
        width = edge_data["line"]["width"]
        opacity = edge_data["opacity"]
        if not all(
            [
                render_type != "highlighted" or color == highlighted_color,
                width == render_type_width,
                opacity == render_type_opacity,
            ]
        ):
            return False
    return True


def _verify_nodes_are_highlighted(tester: FigureTester, nodes: list[str]) -> bool:
    highlighted_color = RENDER_TYPE_SPECS["node"]["highlighted"]["color"]
    highlighted_size = RENDER_TYPE_SPECS["node"]["highlighted"]["size"]
    highlighted_opacity = RENDER_TYPE_SPECS["node"]["highlighted"]["opacity"]
    for node_text in nodes:
        node_data = tester.get_node_data(node_text)
        color = node_data["marker"]["color"]
        size = node_data["marker"]["size"]
        opacity = node_data["opacity"]
        if not all(
            [
                color == highlighted_color,
                size == highlighted_size,
                opacity == highlighted_opacity,
            ]
        ):
            return False
    return True


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
    assert _verify_render_type_of_nodes(tester, selected_nodes, render_type="selected")

    # selected/highlighted edges are part of the atg, other edges are "visual aids"
    # for this case, there are no "highlighted" and "other" edges to check
    selected_edges = [("123", "132"), ("213", "231"), ("312", "321")]
    some_edges_that_dont_exist = [
        ("123", "312"),
        ("123", "321"),
        ("123", "231"),
        ("312", "213"),
    ]
    assert _verify_render_type_of_edges(tester, selected_edges, render_type="selected")
    assert _verify_edges_do_not_exist(tester, some_edges_that_dont_exist)

    # edges are colored according to swap type except highlighted edges
    edge_12 = [("123", "213"), ("312", "321")]
    edge_23 = [("123", "132"), ("231", "321")]
    diff_swap = [("123", "132"), ("123", "213")]
    assert _verify_egdes_have_the_same_color(tester, edge_23)
    assert _verify_egdes_have_the_same_color(tester, edge_12)
    assert not _verify_egdes_have_the_same_color(tester, diff_swap)

    # ============ Size 4 ============ #
    visualizer = PosetVisualizer(4)
    tester = FigureTester(visualizer.get_figure_data())

    # selected/highlighted nodes are part of the atg
    # for this case, there are no "highlighted", "other", and "does not exist" nodes to check
    some_selected_nodes = ["1243", "1432", "2134", "2431", "4312", "3214"]
    assert _verify_render_type_of_nodes(
        tester, some_selected_nodes, render_type="selected"
    )

    # selected/highlighted edges are part of the atg, other edges are "visual aids"
    # for this case, there are no "highlighted" and "other" edges to check
    some_selected_edges = [("1423", "1432"), ("2134", "2143"), ("4312", "4321")]
    some_edges_that_dont_exist = [
        ("1234", "3124"),
        ("1423", "3421"),
        ("1243", "2341"),
        ("4312", "4213"),
    ]
    assert _verify_render_type_of_edges(
        tester, some_selected_edges, render_type="selected"
    )
    assert _verify_edges_do_not_exist(tester, some_edges_that_dont_exist)

    # edges are colored according to swap type except highlighted edges
    edge_14 = [("2143", "2413"), ("3214", "3241"), ("1423", "4123")]
    edge_24 = [("1243", "1423"), ("2413", "4213"), ("1324", "1342")]
    diff_swap = [("1243", "1423"), ("1423", "4123")]
    assert _verify_egdes_have_the_same_color(tester, edge_14)
    assert _verify_egdes_have_the_same_color(tester, edge_24)
    assert not _verify_egdes_have_the_same_color(tester, diff_swap)


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
    assert _verify_render_type_of_nodes(tester, selected_nodes, render_type="selected")
    assert _verify_render_type_of_nodes(tester, other_nodes, render_type="other")

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
    assert _verify_render_type_of_edges(tester, selected_edges, render_type="selected")
    assert _verify_render_type_of_edges(tester, other_edges, render_type="other")
    assert _verify_edges_do_not_exist(tester, some_edges_that_dont_exist)

    # edges are colored according to swap type except highlighted edges
    # in this case, no "selected" edges have the same color
    diff_swap1 = [("123", "132"), ("132", "312")]
    diff_swap2 = [("123", "132"), ("312", "321")]
    diff_swap3 = [("132", "312"), ("312", "321")]
    assert not _verify_egdes_have_the_same_color(tester, diff_swap1)
    assert not _verify_egdes_have_the_same_color(tester, diff_swap2)
    assert not _verify_egdes_have_the_same_color(tester, diff_swap3)

    # ============ Size 4 ============ #
    visualizer = PosetVisualizer(4)
    selected_nodes = TWOMAXIMAL
    visualizer.select_nodes(selected_nodes)
    tester = FigureTester(visualizer.get_figure_data())

    # selected/highlighted nodes are part of the atg
    # for this case, there are no "highlighted" and "does not exist" nodes to check
    selected_nodes = selected_nodes
    some_other_nodes = ["4321", "4231", "2413"]
    assert _verify_render_type_of_nodes(tester, selected_nodes, render_type="selected")
    assert _verify_render_type_of_nodes(tester, some_other_nodes, render_type="other")

    # selected/highlighted edges are part of the atg, other edges are "visual aids"
    # for this case, there are no "highlighted" edges to check
    some_selected_edges = [("2134", "2143"), ("1234", "1324"), ("3142", "3412")]
    some_other_edges = [("4321", "4231"), ("2143", "2413")]
    some_edges_that_dont_exist = [("1243", "3142"), ("4123", "4321"), ("1234", "2314")]
    assert _verify_render_type_of_edges(
        tester, some_selected_edges, render_type="selected"
    )
    assert _verify_render_type_of_edges(tester, some_other_edges, render_type="other")
    assert _verify_edges_do_not_exist(tester, some_edges_that_dont_exist)

    # edges are colored according to swap type except highlighted edges
    edge_24 = [("3124", "3142"), ("1324", "1342"), ("1243", "1423")]
    edge_13 = [("3124", "1324"), ("3142", "1342")]
    edge_23 = [("1423", "1432"), ("1234", "1324")]
    diff_swap = [("2134", "2143"), ("1234", "2134")]
    assert _verify_egdes_have_the_same_color(tester, edge_24)
    assert _verify_egdes_have_the_same_color(tester, edge_13)
    assert _verify_egdes_have_the_same_color(tester, edge_23)
    assert not _verify_egdes_have_the_same_color(tester, diff_swap)


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
    assert _verify_render_type_of_nodes(tester, selected_nodes, render_type="selected")
    assert _verify_render_type_of_nodes(tester, other_nodes, render_type="other")
    assert _verify_render_type_of_nodes(
        tester, highlighted_nodes, render_type="highlighted"
    )

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
    assert _verify_render_type_of_edges(tester, selected_edges, render_type="selected")
    assert _verify_render_type_of_edges(tester, other_edges, render_type="other")
    assert _verify_render_type_of_edges(
        tester, highlighted_edges, render_type="highlighted"
    )
    assert _verify_edges_do_not_exist(tester, some_edges_that_dont_exist)

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
    assert _verify_render_type_of_nodes(tester, selected_nodes, render_type="selected")
    assert _verify_render_type_of_nodes(tester, some_other_nodes, render_type="other")
    assert _verify_render_type_of_nodes(
        tester, highlighted_nodes, render_type="highlighted"
    )

    # selected/highlighted edges are part of the atg, other edges are "visual aids"
    some_selected_edges = [("2134", "2143"), ("1234", "1324"), ("3142", "3412")]
    some_other_edges = [("4321", "4231"), ("2143", "2413")]
    highlighted_edges = [("4123", "1423"), ("1423", "1243"), ("1243", "1234")]
    some_edges_that_dont_exist = [("1243", "3142"), ("4123", "4321"), ("1234", "2314")]
    assert _verify_render_type_of_edges(
        tester, some_selected_edges, render_type="selected"
    )
    assert _verify_render_type_of_edges(tester, some_other_edges, render_type="other")
    assert _verify_render_type_of_edges(
        tester, highlighted_edges, render_type="highlighted"
    )
    assert _verify_edges_do_not_exist(tester, some_edges_that_dont_exist)

    # edges are colored according to swap type except highlighted edges
    edge_24 = [("3124", "3142"), ("1324", "1342")]
    edge_13 = [("3124", "1324"), ("3142", "1342")]
    edge_23 = [("1423", "1432"), ("1234", "1324")]
    diff_swap = [("2134", "2143"), ("1234", "2134")]
    assert _verify_egdes_have_the_same_color(tester, edge_24)
    assert _verify_egdes_have_the_same_color(tester, edge_13)
    assert _verify_egdes_have_the_same_color(tester, edge_23)
    assert not _verify_egdes_have_the_same_color(tester, diff_swap)
