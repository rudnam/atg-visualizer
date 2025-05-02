import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { screen, within } from "@testing-library/react";
import { render } from "../../test-utils/render";
import InputForm from "./InputForm";
import userEvent from "@testing-library/user-event";

describe("InputForm", () => {
  const mockFetchGraphData: () => Promise<void> = vi.fn();
  const mockFetchGraphDataFromCoverRelation: () => Promise<void> = vi.fn();
  const mockFetchPosetCover: () => Promise<void> = vi.fn();

  beforeEach(() => {
    render(
      <InputForm
        fetchGraphData={mockFetchGraphData}
        fetchGraphDataFromCoverRelation={mockFetchGraphDataFromCoverRelation}
        fetchPosetCoverResults={mockFetchPosetCover}
        loading={false}
      />,
    );
  });

  it("renders", () => {
    expect(screen.getByText("INPUT")).toBeInTheDocument();
  });

  describe("with upsilon as input", () => {
    it("renders all form elements", () => {
      expect(screen.getByTestId("input-mode-control")).toBeInTheDocument();
      expect(
        screen.getByTestId("permutation-length-slider"),
      ).toBeInTheDocument();
      expect(screen.getByTestId("input-linear-orders")).toBeInTheDocument();
      expect(screen.getByTestId("draw-button")).toBeInTheDocument();
      expect(screen.getByTestId("solve-button")).toBeInTheDocument();
    });

    it("calls fetchGraphData with correct parameters when Draw button is clicked", async () => {
      const textarea = screen.getByTestId("input-linear-orders");
      await userEvent.type(textarea, "1234\n4321");

      const drawButton = screen.getByTestId("draw-button");
      await userEvent.click(drawButton);

      expect(mockFetchGraphData).toHaveBeenCalledWith(4, "Default", [
        "1234",
        "4321",
      ]);
    });

    it("calls fetchPosetCoverResults with correct parameters when Solve button is clicked", async () => {
      const textarea = screen.getByTestId("input-linear-orders");
      await userEvent.type(textarea, "1234\n4321");

      const solveButton = screen.getByTestId("solve-button");
      await userEvent.click(solveButton);

      expect(mockFetchPosetCover).toHaveBeenCalledWith(4, "Default", 2, [
        "1234",
        "4321",
      ]);
    });
  });

  describe("with poset as input", () => {
    beforeEach(async () => {
      const posetModeButton = within(
        screen.getByTestId("input-mode-control"),
      ).getByText("Poset");
      await userEvent.click(posetModeButton);
    });

    it("renders all form elements", () => {
      expect(screen.getByTestId("input-mode-control")).toBeInTheDocument();
      expect(
        screen.getByTestId("input-select-drawing-method"),
      ).toBeInTheDocument();
      expect(
        screen.getByTestId("permutation-length-slider"),
      ).toBeInTheDocument();
      expect(screen.getByTestId("input-cover-relation")).toBeInTheDocument();
      expect(screen.getByTestId("draw-button")).toBeInTheDocument();
      expect(screen.queryByTestId("solve-button")).not.toBeInTheDocument();
    });

    it("calls fetchGraphData with correct parameters when Draw button is clicked", async () => {
      const textarea = screen.getByTestId("input-cover-relation");
      await userEvent.type(textarea, "1,2\n2,3");

      const drawButton = screen.getByTestId("draw-button");
      await userEvent.click(drawButton);

      expect(mockFetchGraphDataFromCoverRelation).toHaveBeenCalledWith(
        4,
        "Default",
        [
          [1, 2],
          [2, 3],
        ],
      );
    });
  });

  afterEach(() => {
    vi.clearAllMocks();
  });
});
