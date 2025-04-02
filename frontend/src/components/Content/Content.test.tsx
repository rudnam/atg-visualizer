import { afterEach, describe, expect, it, vi } from "vitest";
import { screen, waitFor, within } from "@testing-library/react";
import { render } from "../../test-utils/render";
import Content from "./Content";
import posetService from "../../services/poset";
import userEvent from "@testing-library/user-event";

vi.mock("plotly.js-dist", () => ({
  default: {
    react: vi.fn(),
  },
}));

vi.mock("../../services/poset", () => ({
  default: {
    getAtgGraphData: vi.fn(),
    getAtgGraphDataFromCoverRelation: vi.fn(),
    solveOptimalKPosetCover: vi.fn(),
  },
}));

describe("Content", () => {
  it("renders input form, graph, and results panel", () => {
    render(<Content />);
    expect(screen.getByText("INPUT")).toBeInTheDocument();
    expect(
      screen.getByText("ADJACENT TRANSPOSITION GRAPH"),
    ).toBeInTheDocument();
    expect(screen.getByText("RESULTS")).toBeInTheDocument();
  });

  it("calls getAtgGraphData with correct parameters when draw button is clicked with upsilon as input", async () => {
    render(<Content />);

    const textarea = screen.getByTestId("input-linear-orders");
    await userEvent.type(textarea, "1234\n4321");

    const drawButton = screen.getByTestId("draw-button");
    await userEvent.click(drawButton);

    await waitFor(() =>
      expect(posetService.getAtgGraphData).toHaveBeenCalledWith(4, [
        "1234",
        "4321",
      ]),
    );
  });

  it("calls getAtgGraphData with correct parameters when draw button is clicked with poset as input", async () => {
    render(<Content />);

    const posetModeButton = within(
      screen.getByTestId("input-mode-control"),
    ).getByText("Poset");
    await userEvent.click(posetModeButton);

    const textarea = screen.getByTestId("input-cover-relation");
    await userEvent.type(textarea, "1,2\n2,3");

    const drawButton = screen.getByTestId("draw-button");
    await userEvent.click(drawButton);

    await waitFor(() =>
      expect(
        posetService.getAtgGraphDataFromCoverRelation,
      ).toHaveBeenCalledWith(4, [
        [1, 2],
        [2, 3],
      ]),
    );
  });

  it("calls solveOptimalKPosetCover with correct parameters when solve button is clicked", async () => {
    render(<Content />);

    const textarea = screen.getByTestId("input-linear-orders");
    await userEvent.type(textarea, "1234\n4321");

    const solveButton = screen.getByTestId("solve-button");
    await userEvent.click(solveButton);

    await waitFor(() =>
      expect(posetService.solveOptimalKPosetCover).toHaveBeenCalledWith(2, [
        "1234",
        "4321",
      ]),
    );
  });

  afterEach(() => {
    vi.clearAllMocks();
  });
});
