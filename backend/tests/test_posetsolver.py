from app.posetsolver import PosetSolver


def testPosetSolver():
    linearOrders = ["123", "132", "312", "321"]
    k = 2

    poset_solver = PosetSolver(linearOrders, k)
    result = poset_solver.exact_k_poset_cover(linearOrders, k)

    assert set(result[0]) == set(["312", "123", "132"])
    assert set(result[1]) == set(["312", "321", "132"])


testPosetSolver()
