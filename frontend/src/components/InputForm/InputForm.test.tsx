import { afterEach, describe, expect, it, vi } from "vitest";
import { screen } from "@testing-library/react";
import { render } from "../../test-utils/render";
import InputForm from "./InputForm";
import userEvent from "@testing-library/user-event";

describe("InputForm", () => {
  const mockFetchGraphData: () => Promise<void> = vi.fn();
  const mockFetchPosetCover: () => Promise<void> = vi.fn();

  it("renders", () => {
    render(
      <InputForm
        fetchEntireGraphData={mockFetchGraphData}
        fetchPosetCoverResults={mockFetchPosetCover}
        loading={false}
      />,
    );
    expect(screen.getByText("INPUT")).toBeInTheDocument();
  });

  it("renders all form elements", () => {
    render(
      <InputForm
        fetchEntireGraphData={mockFetchGraphData}
        fetchPosetCoverResults={mockFetchPosetCover}
        loading={false}
      />,
    );

    expect(screen.getByTestId("permutation-length-slider")).toBeInTheDocument();
    expect(screen.getByTestId("input-y")).toBeInTheDocument();
    expect(screen.getByTestId("draw-button")).toBeInTheDocument();
    expect(screen.getByTestId("solve-button")).toBeInTheDocument();
  });

  it("calls fetchEntireGraphData with correct parameters when Draw button is clicked", async () => {
    render(
      <InputForm
        fetchEntireGraphData={mockFetchGraphData}
        fetchPosetCoverResults={mockFetchPosetCover}
        loading={false}
      />,
    );

    const textarea = screen.getByTestId("input-y");
    await userEvent.type(textarea, "1234\n4321");

    const drawButton = screen.getByTestId("draw-button");
    await userEvent.click(drawButton);

    expect(mockFetchGraphData).toHaveBeenCalledWith(4, ["1234", "4321"]);
  });

  it("calls fetchPosetCoverResults with correct parameters when Solve button is clicked", async () => {
    render(
      <InputForm
        fetchEntireGraphData={mockFetchGraphData}
        fetchPosetCoverResults={mockFetchPosetCover}
        loading={false}
      />,
    );

    const textarea = screen.getByTestId("input-y");
    await userEvent.type(textarea, "1234\n4321");

    const solveButton = screen.getByTestId("solve-button");
    await userEvent.click(solveButton);

    expect(mockFetchPosetCover).toHaveBeenCalledWith(4, 2, ["1234", "4321"]);
  });

  afterEach(() => {
    vi.clearAllMocks();
  });
});
