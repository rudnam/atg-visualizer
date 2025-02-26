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
1. test "default" output (i.e. without selection; permutahedron)
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
"""

import pytest

from app.posetvisualizer import PosetVisualizer
from tests.testing_utils import FigureTester


def testPosetVisualizer():
    with pytest.raises(Exception, match="at least 2"):
        PosetVisualizer(1)

    with pytest.raises(Exception, match=f"at most {PosetVisualizer.MAX_SIZE}"):
        PosetVisualizer(PosetVisualizer.MAX_SIZE + 1)

    with pytest.raises(TypeError, match="must be an integer"):
        PosetVisualizer("4")

    # ============ Size 3 ============ #
    visualizer = PosetVisualizer(3)
    tester = FigureTester(visualizer.get_figure_data())

    # Edges only exist between adjacent swaps
    assert tester.get_edge_data("123", "132") != None
    assert tester.get_edge_data("123", "321") == None

    # Edges are colored according to swap type
    assert (
        tester.get_edge_data("123", "132")["line"]["color"]
        == tester.get_edge_data("231", "321")["line"]["color"]
    )
    assert (
        tester.get_edge_data("123", "132")["line"]["color"]
        != tester.get_edge_data("123", "213")["line"]["color"]
    )

    # ============ Size 4 ============ #
    visualizer = PosetVisualizer(4)
    tester = FigureTester(visualizer.get_figure_data())

    # Edges only exist between adjacent swaps
    assert tester.get_edge_data("1234", "1324") != None
    assert tester.get_edge_data("1234", "3214") == None

    # Edges are colored according to swap type
    assert (
        tester.get_edge_data("1234", "1324")["line"]["color"]
        == tester.get_edge_data("4231", "4321")["line"]["color"]
    )
    assert (
        tester.get_edge_data("1234", "1324")["line"]["color"]
        != tester.get_edge_data("1234", "2134")["line"]["color"]
    )
