import pytest

from app.posetvisualizer import PosetVisualizer


def testPosetVisualizer():
    with pytest.raises(Exception, match="at least 2"):
        PosetVisualizer(1)

    with pytest.raises(Exception, match=f"at most {PosetVisualizer.MAX_SIZE}"):
        PosetVisualizer(PosetVisualizer.MAX_SIZE + 1)

    with pytest.raises(TypeError, match="must be an integer"):
        PosetVisualizer("4")
