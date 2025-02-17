import { beforeEach, describe, expect, test, vi } from "vitest";
import { fireEvent, screen } from "@testing-library/react";
import { render } from "../../test-utils/render";
import ResultsPanel from "./ResultsPanel";
import { PosetResult } from "../../types";
import { useState } from "react";

describe("ResultsPanel", () => {
  const mockResults: PosetResult[] = [
    {
      name: "P1",
      relations: [
        [2, 4],
        [1, 3],
        [3, 4],
        [1, 4],
      ],
      linearExtensions: ["1324", "3124", "1234"],
    },
    {
      name: "P2",
      relations: [
        [2, 4],
        [1, 3],
        [3, 4],
        [1, 4],
      ],
      linearExtensions: ["1324", "1234", "2134"],
    },
  ];
  let setHighlightedPosetIndex: React.Dispatch<React.SetStateAction<number>>;

  beforeEach(() => {
    setHighlightedPosetIndex = vi.fn();
  });

  test("renders", () => {
    render(
      <ResultsPanel
        posetResults={[]}
        highlightedPosetIndex={-1}
        setHighlightedPosetIndex={setHighlightedPosetIndex}
      />
    );
    expect(screen.getByText("RESULTS")).toBeInTheDocument();
  });

  test("renders with correct number of items", () => {
    render(
      <ResultsPanel
        posetResults={mockResults}
        highlightedPosetIndex={-1}
        setHighlightedPosetIndex={setHighlightedPosetIndex}
      />
    );

    const items = screen.getAllByTestId("poset-result-component");
    expect(items).toHaveLength(mockResults.length);
  });

  test("renders linear extensions correctly", () => {
    render(
      <ResultsPanel
        posetResults={mockResults}
        highlightedPosetIndex={-1}
        setHighlightedPosetIndex={setHighlightedPosetIndex}
      />
    );

    const extensions = screen.getAllByTestId(
      "poset-result-component-linear-extensions"
    );
    expect(extensions[0]).toHaveTextContent(mockResults[0].linearExtensions[0]);
    expect(extensions[0]).toHaveTextContent(mockResults[0].linearExtensions[1]);

    expect(extensions[1]).toHaveTextContent(mockResults[1].linearExtensions[0]);
    expect(extensions[1]).toHaveTextContent(mockResults[1].linearExtensions[1]);
  });

  test("applies correct button variant based on highlight state", () => {
    render(
      <ResultsPanel
        posetResults={mockResults}
        highlightedPosetIndex={1}
        setHighlightedPosetIndex={setHighlightedPosetIndex}
      />
    );

    const items = screen.getAllByTestId("poset-result-component-button");
    expect(items[0]).toHaveAttribute("data-variant", "outline");
    expect(items[1]).toHaveAttribute("data-variant", "filled");
  });

  test("clicking an item highlights it and clicking again unhighlights it", () => {
    function Wrapper() {
      const [index, setIndex] = useState(-1);
      return (
        <ResultsPanel
          posetResults={mockResults}
          highlightedPosetIndex={index}
          setHighlightedPosetIndex={setIndex}
        />
      );
    }

    render(<Wrapper />);

    const firstItem = screen.getAllByTestId("poset-result-component-button")[0];

    expect(firstItem).toHaveAttribute("data-variant", "outline");

    fireEvent.click(firstItem);
    expect(firstItem).toHaveAttribute("data-variant", "filled");

    fireEvent.click(firstItem);
    expect(firstItem).toHaveAttribute("data-variant", "outline");
  });
});
