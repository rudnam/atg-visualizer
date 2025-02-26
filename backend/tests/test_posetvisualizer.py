import pytest

from backend.app.posetvisualizer import PosetVisualizer
from backend.tests.testing_utils import FigureTester


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
