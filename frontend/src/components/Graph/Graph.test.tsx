import { describe, expect, it, vi } from "vitest";
import { screen } from "@testing-library/react";
import { render } from "../../test-utils/render";
import Graph from "./Graph";
import GraphComponent from "./Graph";
import Plotly from "plotly.js-dist";
import { GraphData } from "../../types";

vi.mock("plotly.js-dist", () => ({
  default: {
    react: vi.fn(),
  },
}));

describe("Graph", () => {
  it("renders", () => {
    render(<Graph loading={false} graphData={null} />);
    expect(screen.getByText("ADJACENT TRANSPOSITION GRAPH")).toBeDefined();
  });

  it("calls Plotly.react when graphData is provided", () => {
    const mockGraphData = {
      data: [{ x: [1, 2, 3], y: [3, 2, 1], type: "scatter" }],
      layout: { title: "Test Graph" },
    } as GraphData;

    render(<GraphComponent loading={false} graphData={mockGraphData} />);

    expect(Plotly.react).toHaveBeenCalledWith(
      expect.any(HTMLElement),
      mockGraphData.data,
      mockGraphData.layout,
      expect.objectContaining({ displaylogo: false }),
    );
  });
});
