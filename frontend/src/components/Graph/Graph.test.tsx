import { describe, expect, test, vi } from "vitest";
import { screen } from "@testing-library/react";
import { render } from "../../test-utils/render";
import Graph from "./Graph";

vi.mock("plotly.js-dist", () => ({
  react: vi.fn(),
}));

describe("Graph", () => {
  test("renders", () => {
    render(<Graph loading={false} graphData={null} />);
    expect(screen.getByText("ADJACENT TRANSPOSITION GRAPH")).toBeDefined();
  });
});
