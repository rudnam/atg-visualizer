import { describe, expect, it } from "vitest";
import { screen } from "@testing-library/react";
import { render } from "../../test-utils/render";
import Graph from "./Graph";
import GraphComponent from "./Graph";
import { GraphData } from "../../types";

describe("Graph", () => {
  it("renders", () => {
    render(<Graph loading={false} graphData={null} />);
    expect(
      screen.getByText("ADJACENT TRANSPOSITION GRAPH"),
    ).toBeInTheDocument();
  });

  it("shows loading overlay when loading is true", () => {
    render(<GraphComponent loading={true} graphData={null} />);
    expect(
      screen.getByText("ADJACENT TRANSPOSITION GRAPH"),
    ).toBeInTheDocument();
    expect(screen.getByTestId("loading-overlay")).toBeInTheDocument();
  });

  it("renders Plotly graph when graphData is provided", () => {
    const mockGraphData = {
      data: [{ x: [1, 2, 3], y: [3, 2, 1], type: "scatter" }],
      layout: { title: "Test Graph" },
    } as GraphData;

    render(<GraphComponent loading={false} graphData={mockGraphData} />);
    expect(screen.getByTestId("plot-container")).toBeInTheDocument();
  });

  it("does not render Plotly graph when graphData is null", () => {
    render(<GraphComponent loading={false} graphData={null} />);
    expect(screen.queryByTestId("plot-container")).not.toBeInTheDocument();
  });
});
