from app.classes import EdgeData, FigureData, NodeData


class FigureTester:
    def __init__(self, figure_data: FigureData):
        required_keys = {"data", "layout"}
        if not all(key in figure_data for key in required_keys):
            raise ValueError(
                f"Invalid FigureData: Missing keys. Expected {required_keys}, got {figure_data.keys()}"
            )

        self._data = [x.to_plotly_json() for x in figure_data["data"]]
        self._layout = figure_data["layout"]

    def get_node_data(self, text: str) -> NodeData | None:
        """Find a node by its text."""

        for trace in self._data:
            is_node_trace = "markers" in trace.get("mode", "")
            if not is_node_trace:
                continue

            for i, node_text in enumerate(trace["text"]):
                if str(node_text) != text:
                    continue

                return NodeData(
                    hoverinfo=trace["hoverinfo"],
                    marker=trace["marker"],
                    mode=trace["mode"],
                    name=trace["name"],
                    opacity=trace["opacity"],
                    showlegend=trace["showlegend"],
                    text=trace["text"][i],
                    textposition=trace["textposition"],
                    x=trace["x"][i],
                    y=trace["y"][i],
                    z=trace["z"][i],
                )
        return None

    def get_edge_data(self, n1: str, n2: str) -> EdgeData | None:
        """Find an edge by the text of its nodes."""

        for trace in self._data:
            is_edge_trace = "lines" in trace.get("mode", "")
            if not is_edge_trace:
                continue

            for i in range(0, len(trace["x"]), 3):
                start_node = self.get_node_data_by_position(
                    trace["x"][i], trace["y"][i], trace["z"][i]
                )
                end_node = self.get_node_data_by_position(
                    trace["x"][i + 1], trace["y"][i + 1], trace["z"][i + 1]
                )

                if not start_node or not end_node:
                    continue
                if not (start_node["text"] == n1 and end_node["text"] == n2) and not (
                    start_node["text"] == n2 and end_node["text"] == n1
                ):
                    continue

                return EdgeData(
                    hoverinfo=trace["hoverinfo"],
                    line=trace["line"],
                    mode=trace["mode"],
                    name=trace["name"],
                    opacity=trace["opacity"],
                    showlegend=trace["showlegend"],
                    x=(trace["x"][i], trace["x"][i + 1]),
                    y=(trace["y"][i], trace["x"][i + 1]),
                    z=(trace["z"][i], trace["x"][i + 1]),
                )
        return None

    def get_node_data_by_position(
        self, x: float, y: float, z: float
    ) -> NodeData | None:
        """Find a node by its (x, y, z) coordinates."""

        for trace in self._data:
            is_node_trace = "markers" in trace.get("mode", "")
            if not is_node_trace:
                continue

            for i in range(len(trace["text"])):
                if (trace["x"][i], trace["y"][i], trace["z"][i]) != (x, y, z):
                    continue

                return NodeData(
                    hoverinfo=trace["hoverinfo"],
                    marker=trace["marker"],
                    mode=trace["mode"],
                    name=trace["name"],
                    opacity=trace["opacity"],
                    showlegend=trace["showlegend"],
                    text=trace["text"][i],
                    textposition=trace["textposition"],
                    x=trace["x"][i],
                    y=trace["y"][i],
                    z=trace["z"][i],
                )
        return None
