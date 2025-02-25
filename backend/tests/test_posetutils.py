import pytest
import networkx as nx
from app.posetutils import PosetUtils
from app.classes import *


def test_get_atg_from_upsilon():
    f = PosetUtils.get_atg_from_upsilon

    # upsilon is a "path" LEG
    upsilon = ["1234", "1243", "1423", "4123"]
    G = f(upsilon)
    assert set(G.nodes()) == {"1234", "1243", "1423", "4123"}
    expected_edges = [("1234", "1243"), ("1243", "1423"), ("1423", "4123")]
    assert all([G.has_edge(*e) for e in expected_edges])

    # upsilon has no edges
    upsilon = ["1234", "2143", "3124", "1342", "1423", "4132"]
    G = f(upsilon)
    assert set(G.nodes()) == {"1234", "2143", "3124", "1342", "1423", "4132"}
    assert len(G.edges()) == 0


def test_get_linear_extensions_from_graph():
    f = PosetUtils.get_linear_extensions_from_graph

    # this hasse graph will result in a square linear extension graph
    nodes = range(1, 5)
    cover_relation: CoverRelation = [(1, 3), (1, 4), (2, 3), (2, 4)]
    my_hasse: HasseDiagram = nx.DiGraph()
    my_hasse.add_nodes_from(nodes)
    my_hasse.add_edges_from(cover_relation)
    assert {"1234", "1243", "2134", "2143"} == set(f(my_hasse))

    "1 → 2 → 3 → 4 → 5"
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
    my_dag: AcyclicDiGraph = nx.DiGraph()
    my_dag.add_nodes_from(nodes)
    my_dag.add_edges_from(partial_order)
    assert {"12345"} == set(f(my_dag))


def test_get_linear_extensions_from_relation():
    f = PosetUtils.get_linear_extensions_from_relation
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
    sequence = "12345"
    assert set(f(partial_order, sequence)) == {"12345"}

    """ 1---→ 4---→ 5
         ↘        ↗
           2---→ 3
    """
    cover_relation: CoverRelation = [
        (1, 2),
        (2, 3),
        (3, 5),
        (1, 4),
        (4, 5),
    ]
    sequence = "12345"
    assert set(f(cover_relation, sequence)) == {"14235", "12435", "12345"}


def test_get_graph_from_relation():
    # Did I use this function? Apparently, G is either HasseDiagram or AcyclicDiGraph which is undesirable
    f = PosetUtils.get_graph_from_relation
    cover_relation: CoverRelation = [(1, 3), (2, 3)]
    sequence = "1234"
    G = f(cover_relation, sequence)

    assert {1, 2, 3, 4} == set(G.nodes())
    assert (1, 3) in G.edges()
    assert (2, 3) in G.edges()

    # test for partial order input?


def test_get_hasse_from_partial_order():
    f = PosetUtils.get_hasse_from_partial_order

    "1 → 2 → 3 → 4 → 5"
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
    sequence = "12345"
    G = f(partial_order, sequence)

    assert {1, 2, 3, 4, 5} == set(G.nodes())
    assert {(1, 2), (2, 3), (3, 4), (4, 5)} == set(G.edges())


def test_ancestors():
    f = PosetUtils.ancestors

    nodes = range(1, 5)
    cover_relation: CoverRelation = [(1, 3), (2, 3)]
    my_hasse: HasseDiagram = nx.DiGraph()
    my_hasse.add_nodes_from(nodes)
    my_hasse.add_edges_from(cover_relation)

    assert set(f(3, my_hasse)) == {1, 2}
    assert len(f(1, my_hasse)) == 0
    assert len(f(4, my_hasse)) == 0

    "1 → 2 → 3 → 4 → 5"
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
    my_dag: AcyclicDiGraph = nx.DiGraph()
    my_dag.add_nodes_from(nodes)
    my_dag.add_edges_from(partial_order)

    assert set(f(5, my_dag)) == {1, 2, 3, 4}
    assert set(f(4, my_dag)) == {1, 2, 3}
    assert set(f(2, my_dag)) == {1}
    assert len(f(1, my_dag)) == 0


def test_descendants():
    f = PosetUtils.descendants

    nodes = range(1, 5)
    cover_relation: CoverRelation = [(1, 3), (2, 3)]
    my_hasse: HasseDiagram = nx.DiGraph()
    my_hasse.add_nodes_from(nodes)
    my_hasse.add_edges_from(cover_relation)

    assert set(f(1, my_hasse)) == {3}
    assert set(f(2, my_hasse)) == {3}
    assert 3 not in f(3, my_hasse)
    assert len(f(1, my_hasse)) == 1
    assert len(f(4, my_hasse)) == 0

    "1 → 2 → 3 → 4 → 5"
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
    my_dag: AcyclicDiGraph = nx.DiGraph()
    my_dag.add_nodes_from(nodes)
    my_dag.add_edges_from(partial_order)

    assert set(f(1, my_dag)) == {2, 3, 4, 5}
    assert set(f(2, my_dag)) == {3, 4, 5}
    assert set(f(3, my_dag)) == {4, 5}
    assert len(f(5, my_dag)) == 0


def test_hasse_dist():
    f = PosetUtils.hasse_dist

    nodes = range(1, 5)
    cover_relation: CoverRelation = [(1, 3), (2, 3)]
    my_hasse: HasseDiagram = nx.DiGraph()
    my_hasse.add_nodes_from(nodes)
    my_hasse.add_edges_from(cover_relation)

    assert f(my_hasse, 1, 3) == 1
    assert f(my_hasse, 1, 2) == float("inf")
    assert f(my_hasse, 2, 3) == f(my_hasse, 3, 2)

    """ 1---→ 4---→ 5
         ↘        ↗
           2---→ 3
    """
    nodes = range(1, 6)
    cover_relation: CoverRelation = [
        (1, 2),
        (2, 3),
        (3, 5),
        (1, 4),
        (4, 5),
    ]
    my_hasse: HasseDiagram = nx.DiGraph()
    my_hasse.add_nodes_from(nodes)
    my_hasse.add_edges_from(cover_relation)

    assert f(my_hasse, 5, 1) == 2
    assert f(my_hasse, 1, 5) == 2
    assert f(my_hasse, 4, 3) == float("inf")
    assert f(my_hasse, 3, 1) == 2


def test_covers():
    # I believe this function was not used
    f = PosetUtils.covers
    nodes = range(1, 6)
    cover_relation: CoverRelation = [
        (1, 2),
        (2, 3),
        (3, 5),
        (1, 4),
        (4, 5),
    ]
    my_hasse: HasseDiagram = nx.DiGraph()
    my_hasse.add_nodes_from(nodes)
    my_hasse.add_edges_from(cover_relation)

    assert f(my_hasse, 1, 4) == True
    assert f(my_hasse, 4, 1) == False
    assert f(my_hasse, 1, 3) == False


def test_x_is_covered_by_y_in_L():
    f = PosetUtils.x_is_covered_by_y_in_L
    assert f("1234", 1, 2) == True
    assert f("3124", 3, 4) == False
    assert f("21435", 5, 3) == False
    assert f("21435", 1, 4) == True


def test_x_is_less_than_y_in_L():
    f = PosetUtils.x_is_less_than_y_in_L
    assert f("1234", 1, 2) == True
    assert f("3124", 3, 4) == True
    assert f("21435", 5, 3) == False
    assert f("21435", 1, 4) == True


def test_swap_xy_in_L():
    f = PosetUtils.swap_xy_in_L
    assert f("1234", 1, 2) == "2134"
    assert f("21435", 3, 5) == "21453"
    assert f("21435", 1, 4) == "24135"

    with pytest.raises(ValueError) as excinfo:
        f("3124", 3, 4)
    assert excinfo.type is ValueError


def test_edge_label():
    f = PosetUtils.edge_label
    assert f("51234", "51324") == {2, 3}
    assert f("4123", "1423") == {1, 4}
    assert f("1234", "2143") is None

    with pytest.raises(ValueError) as excinfo:
        f("3124", "12")
    assert excinfo.type is ValueError


def test_generate_convex():
    f = PosetUtils.generate_convex
    assert set(f(["1234", "1243", "2134"])) == {"1234", "1243", "2134", "2143"}
    assert f(["123"]) == ["123"]
    assert set(f(["1234", "1243", "1423", "4123"])) == {"1234", "1243", "1423", "4123"}
    assert set(f(["1234", "1243", "1423", "1432"])) == {
        "1234",
        "1243",
        "1423",
        "1432",
        "1342",
        "1324",
    }
    with pytest.raises(ValueError) as excinfo:
        f([])
    assert excinfo.type is ValueError


def test_get_partial_order_of_convex():
    f = PosetUtils.get_partial_order_of_convex
    assert set(f(["1234", "1243", "2134"])) == {(1, 3), (1, 4), (2, 3), (2, 4)}
    assert set(f(["1234", "1243", "1423", "1432"])) == {(1, 2), (1, 3), (1, 4)}
    with pytest.raises(ValueError) as excinfo:
        f([])
    assert excinfo.type is ValueError
