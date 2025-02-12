import { describe, expect, test, vi } from "vitest";
import { screen } from "@testing-library/react";
import { render } from "../../test-utils/render";
import ResultsPanel from "./ResultsPanel";

describe("ResultsPanel", () => {
  test("renders", () => {
    const mockHighlightedPosetIndex: () => Promise<void> = vi.fn();
    render(
      <ResultsPanel
        posetResults={[]}
        highlightedPosetIndex={0}
        setHighlightedPosetIndex={mockHighlightedPosetIndex}
      />
    );
    expect(screen.getByText("RESULTS")).toBeDefined();
  });
});
