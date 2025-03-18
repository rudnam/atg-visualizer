from app.posetgraph import PosetGraph
from tests.testing_utils import FigureTester
from tests.test_posetvisualizer import (
    verify_edges_have_the_same_color,
    verify_edges_have_different_colors,
    verify_edges_do_not_exist,
    verify_render_type_of_nodes,
    verify_render_type_of_edges,
)

from .upsilon_constants import TWOMAXIMAL


def test_posetgraph():
    LINEAR_EXTENSIONS = ["1234", "1243", "1324", "1342", "1423", "1432", "4123", "4132"]

    cover_relation = [(1, 2), (1, 3)]
    permutation_length = 4
    posetgraph = PosetGraph(cover_relation, permutation_length)
    tester = FigureTester(posetgraph.get_figure_data())

    assert set(posetgraph.linear_extensions) == set(LINEAR_EXTENSIONS)

    # selected/highlighted nodes are part of the atg
    # for this case, there are no "does not exist" nodes to check
    selected_nodes = LINEAR_EXTENSIONS
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
