"""
Test Overview

PosetSolver Class Methods
 - solve    => ✗ will not be tested; reason: unofficial/not complete
 - minimum_poset_cover  =>  ✓ for testing
 - minimum_poset_cover_of_connected_component   =>  ✗ will not be tested; reason: can be privitized
 - exact_k_poset_cover  =>  ✓ for testing
 - maximal_poset    =>  ✓ for testing 
 
Approach: hand-crafted tests
Issue with code: The class methods for testing can be treated as static methods so class initialization is irrelevant.

Short Description of Chosen Upsilons
Upsilons from "A Parameterized Algorithm for the Poset Cover Problem"
GENMAXIMAL. This was the example upsilon for demonsrating the generalized maximal poset algorithm. Optimal Cost: k=2.
LINE295. Quote, "There is no feasible solution of size 3 but there is a feasible solution of size 2." This is a square LEG. Optimal Cost: k=1.

Upsilons from "A Polynomial Time Algorithm for the 2-Poset Cover Problem"
TWOMAXIMAL. This was the example upsilon for demonstrating the maximal poset algorithm for the 2-poset case. Optimal Cost: k=3.

Other Upsilons
CUBELEG. Edge case for many-linear-orders-but-only-one-poset cover. Optimal Cost: k=1.
SINGLESIX. Edge case for the single linear order. Optimal Cost: k=1.
HEX2SUNGAY. A case for 3-poset cover. Optimal Cost: k=3.

SUMMARY OF ISSUES/CONCERNS
1. Issues with how PosetSolver was written (class-based or static methods?)
2. [minor] Clarification for exact-k behavior when k-1 > number_of_swap_x2
3. PT* should not keep duplicates. Slightly significant refactor as frozenset seems to be a nice solution for this
4. [minor] consultation with mam. bakit po need ng anchor pairs? for example, isn't it sufficient to use a "seed poset"?
5. Implied refactoring, particularly in the signatures of the methods
"""

from app.posetsolver import PosetSolver
from app.posetutils import PosetUtils
from app.classes import *
from .upsilon_constants import (
    TWOMAXIMAL,
    GENMAXIMAL,
    SQHEXPLUSLINE,
    LINE295,
    CUBELEG,
    SINGLESIX,
    HEX2SUNGAY,
)


def test_minimum_poset_cover():
    solver = PosetSolver(upsilon=[])
    poset_cover = solver.minimum_poset_cover(TWOMAXIMAL)
    assert set(TWOMAXIMAL) == set.union(*(set(leg) for leg in poset_cover))
    assert len(poset_cover) == 3

    poset_cover = solver.minimum_poset_cover(GENMAXIMAL)
    assert set(GENMAXIMAL) == set.union(*(set(leg) for leg in poset_cover))
    assert len(poset_cover) == 2

    poset_cover = solver.minimum_poset_cover(SQHEXPLUSLINE)
    assert set(SQHEXPLUSLINE) == set.union(*(set(leg) for leg in poset_cover))
    assert len(poset_cover) == 2

    poset_cover = solver.minimum_poset_cover(LINE295)
    assert set(LINE295) == set.union(*(set(leg) for leg in poset_cover))
    assert len(poset_cover) == 1

    poset_cover = solver.minimum_poset_cover(CUBELEG)
    assert set(CUBELEG) == set.union(*(set(leg) for leg in poset_cover))
    assert len(poset_cover) == 1

    poset_cover = solver.minimum_poset_cover(SINGLESIX)
    assert set(SINGLESIX) == set.union(*(set(leg) for leg in poset_cover))
    assert len(poset_cover) == 1

    poset_cover = solver.minimum_poset_cover(HEX2SUNGAY)
    assert set(HEX2SUNGAY) == set.union(*(set(leg) for leg in poset_cover))
    assert len(poset_cover) == 3


def test_exact_k_poset_cover():
    solver = PosetSolver(upsilon=[])
    k_poset_cover = solver.exact_k_poset_cover(TWOMAXIMAL, 1)
    assert k_poset_cover is None
    k_poset_cover = solver.exact_k_poset_cover(TWOMAXIMAL, 2)
    assert k_poset_cover is None
    k_poset_cover = solver.exact_k_poset_cover(TWOMAXIMAL, 3)
    assert set(TWOMAXIMAL) == set.union(*(set(leg) for leg in k_poset_cover))
    assert len(k_poset_cover) == 3

    k_poset_cover = solver.exact_k_poset_cover(GENMAXIMAL, 1)
    assert k_poset_cover is None
    k_poset_cover = solver.exact_k_poset_cover(GENMAXIMAL, 2)
    assert set(GENMAXIMAL) == set.union(*(set(leg) for leg in k_poset_cover))
    assert len(k_poset_cover) == 2

    # exact_k_poset_cover does not accept disconnected graph inputs like SQHEXPLUSLINE

    k_poset_cover = solver.exact_k_poset_cover(LINE295, 1)
    assert set(LINE295) == set.union(*(set(leg) for leg in k_poset_cover))
    assert len(k_poset_cover) == 1
    k_poset_cover = solver.exact_k_poset_cover(LINE295, 2)
    assert set(LINE295) == set.union(*(set(leg) for leg in k_poset_cover))
    assert len(k_poset_cover) == 2

    # k_poset_cover = solver.exact_k_poset_cover(LINE295, 3)
    # assert k_poset_cover is None
    # oh no. dapat pala unique yung laman ng PT*
    # next time nalang ayusin

    # undefined behavior for the following; needs consultation
    # k_poset_cover = solver.exact_k_poset_cover(LINE295, 3)
    #   it is expected to not get any result according to line 296
    #   however, the algorithm returns None because it never gets to test any set of anchor pairs canonically
    #   this is due to the fact that a square LEG only has two swaps => four tuples to choose from
    #   !! my mistake. this should be possible because the choice is k-1 i.e. A_star = combinations(fourtuples, 3-1=2)
    #
    # k_poset_cover = solver.exact_k_poset_cover(LINE295, 4)
    #   same case as above; this is now applicable as A_star = combinations(fourtuples, 3) => some cycle like (12,21,34) which no L will satisfy
    #   but, however, an answer is expected i.e. all of the four vertices

    k_poset_cover = solver.exact_k_poset_cover(CUBELEG, 1)
    assert set(CUBELEG) == set.union(*(set(leg) for leg in k_poset_cover))
    assert len(k_poset_cover) == 1
    # testing for k>=2 is dubious because PT* contains duplicates
    # moreover, PT* will always contains copies of the single maximal poset, the cubeleg!

    k_poset_cover = solver.exact_k_poset_cover(SINGLESIX, 1)
    assert set(SINGLESIX) == set.union(*(set(leg) for leg in k_poset_cover))
    assert len(k_poset_cover) == 1

    k_poset_cover = solver.exact_k_poset_cover(HEX2SUNGAY, 1)
    assert k_poset_cover is None
    k_poset_cover = solver.exact_k_poset_cover(HEX2SUNGAY, 2)
    assert k_poset_cover is None
    k_poset_cover = solver.exact_k_poset_cover(HEX2SUNGAY, 3)
    assert set(HEX2SUNGAY) == set.union(*(set(leg) for leg in k_poset_cover))
    assert len(k_poset_cover) == 3


def test_maxmimal_poset():
    # list of possible maximal posets using TWOMAXIMAL
    # these are listed due to the fact that the result of maximal_poset is ambiguous that is,
    #   it can result to any of the following so long as the "seed" is a subset of the maximal posets
    #   and all maximal posets are of equal distance to the seed.
    _2134_SQHEX = ["2134", "2143", "1342", "1324", "1234", "1432", "1423", "1243"]
    _3124_SQHEX = ["3142", "3124", "1342", "1324", "1234", "1432", "1423", "1243"]
    _3412_DOWN_TO_1234 = ["3412", "3142", "3124", "1342", "1324", "1234"]
    _4123_SNAKE = ["4123", "1423", "1243", "1234"]

    # for TWOMAXIMAL, we simulate k=3, meaning there are 2 anchor pairs
    solver = PosetSolver(upsilon=[])
    seed_poset: list[LinearOrder] = ["2134"]
    anchor_pairs: list[AnchorPair] = [(2, 1), (3, 4)]
    partial_order: PartialOrder = PosetUtils.get_partial_order_of_convex(seed_poset)
    maximal = solver.maximal_poset(TWOMAXIMAL, anchor_pairs, partial_order)
    assert set(maximal) == set(_2134_SQHEX)

    seed_poset: list[LinearOrder] = ["3142", "3412"]
    anchor_pairs: list[AnchorPair] = [(4, 2), (3, 1)]
    partial_order: PartialOrder = PosetUtils.get_partial_order_of_convex(seed_poset)
    maximal = solver.maximal_poset(TWOMAXIMAL, anchor_pairs, partial_order)
    assert set(maximal) == set(_3412_DOWN_TO_1234)

    # consultation with mam. bakit po need ng anchor pairs? for example, isn't it sufficient
    #   to use a "seed poset"?

    seed_poset: list[LinearOrder] = ["4123", "1423"]
    anchor_pairs: list[AnchorPair] = [(4, 2), (2, 3)]
    partial_order: PartialOrder = PosetUtils.get_partial_order_of_convex(seed_poset)
    maximal = solver.maximal_poset(TWOMAXIMAL, anchor_pairs, partial_order)
    assert set(maximal) == set(_4123_SNAKE)

    seed_poset: list[LinearOrder] = ["1432"]
    anchor_pairs: list[AnchorPair] = [(3, 2), (4, 3)]
    partial_order: PartialOrder = PosetUtils.get_partial_order_of_convex(seed_poset)
    maximal = solver.maximal_poset(TWOMAXIMAL, anchor_pairs, partial_order)
    assert set(maximal) == set(_3124_SQHEX)
