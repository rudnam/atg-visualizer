import { describe, expect, test, vi } from "vitest";
import { screen } from "@testing-library/react";
import { render } from "../../test-utils/render";
import InputForm from "./InputForm";

describe("InputForm", () => {
  test("renders", () => {
    const mockFetchGraphData: () => Promise<void> = vi.fn();
    const mockFetchPosetCover: () => Promise<void> = vi.fn();
    render(
      <InputForm
        fetchEntireGraphData={mockFetchGraphData}
        fetchPosetCoverResults={mockFetchPosetCover}
      />
    );
    expect(screen.getByText("INPUT")).toBeDefined();
  });
});
