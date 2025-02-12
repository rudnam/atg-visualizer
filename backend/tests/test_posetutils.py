import networkx as nx
from app.posetutils import PosetUtils
from app.classes import *


def test_get_linear_extensions_from_graph():
    poset_utils = PosetUtils()
    pass


def test_get_linear_extensions_from_relation():
    pass


def test_get_graph_from_relation():
    pass


def test_get_hasse_from_partial_order():
    pass


def test_ancestors():
    f = PosetUtils.ancestors

    nodes = range(1, 5)
    cover_relation: CoverRelation = [(1, 3), (2, 3)]
    my_hasse: HasseDiagram = nx.DiGraph()
    my_hasse.add_nodes_from(nodes)
    my_hasse.add_edges_from(cover_relation)

    assert 1 in f(3, my_hasse)
    assert 2 in f(3, my_hasse)
    assert 3 not in f(3, my_hasse)
    assert 4 not in f(3, my_hasse)
    assert len(f(1, my_hasse)) == 0
    assert len(f(4, my_hasse)) == 0

    nodes = range(1, 6)
    partial_order: PartialOrder = [
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 5),
        (2, 3),
        (2, 4),
        (2, 5),
        (3, 4),
        (3, 5),
        (4, 5),
    ]
    my_dag: DiGraph = nx.DiGraph()
    my_dag.add_nodes_from(nodes)
    my_dag.add_edges_from(partial_order)

    assert 1 in f(5, my_dag)
    assert 2 in f(4, my_dag)
    assert 3 not in f(2, my_dag)
    assert len(f(1, my_dag)) == 0


def test_descendants():
    f = PosetUtils.descendants

    nodes = range(1, 5)
    cover_relation: CoverRelation = [(1, 3), (2, 3)]
    my_hasse: HasseDiagram = nx.DiGraph()
    my_hasse.add_nodes_from(nodes)
    my_hasse.add_edges_from(cover_relation)

    assert 3 in f(1, my_hasse)
    assert 3 in f(2, my_hasse)
    assert 3 not in f(3, my_hasse)
    assert 4 not in f(1, my_hasse)
    assert len(f(1, my_hasse)) == 1
    assert len(f(4, my_hasse)) == 0

    nodes = range(1, 6)
    partial_order: PartialOrder = [
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 5),
        (2, 3),
        (2, 4),
        (2, 5),
        (3, 4),
        (3, 5),
        (4, 5),
    ]
    my_dag: DiGraph = nx.DiGraph()
    my_dag.add_nodes_from(nodes)
    my_dag.add_edges_from(partial_order)

    assert 5 in f(1, my_dag)
    assert 4 in f(2, my_dag)
    assert 2 not in f(3, my_dag)
    assert len(f(5, my_dag)) == 0


def test_hasse_dist():
    pass


def test_covers():
    pass


def test_x_is_covered_by_y_in_L():
    pass


def test_x_is_less_than_y_in_L():
    pass


def test_swap_xy_in_L():
    pass


def test_edge_label():
    # this function was never used
    pass


def test_generate_convex():
    pass


def test_get_partial_order_of_convex():
    pass
