from app.posetvisualizer import PosetVisualizer
from app.posetutils import PosetUtils

from app.classes import *


class PosetGraph:

    def __init__(self, cover_relation: CoverRelation, permutation_length: int) -> None:
        """PosetLinearExtensionGraph

        Make the drawing of the LEG of a poset specified by its cover relation and permutation length
        Args:
            cover_relation: A list of ordered pairs of the form (a,b)
            permutation_length: The length of the linear orders that are expected to be generated
        """
        self.poset_visualizer = PosetVisualizer(permutation_length)
        sequence: str = "".join(map(str, range(1, permutation_length + 1)))
        self.linear_extensions: LinearExtensions = (
            PosetUtils.get_linear_extensions_from_relation(cover_relation, sequence)
        )
        self.poset_visualizer.select_nodes(self.linear_extensions)

    def get_figure_data(self):
        """Gets the figure data."""
        return self.poset_visualizer.get_figure_data()
