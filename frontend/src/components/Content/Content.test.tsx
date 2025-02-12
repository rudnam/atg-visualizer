import { describe, expect, test, vi } from "vitest";
import { screen } from "@testing-library/react";
import { render } from "../../test-utils/render";
import Content from "./Content";

vi.mock("plotly.js-dist", () => ({
  react: vi.fn(),
}));

describe("Content", () => {
  test("renders", () => {
    render(<Content />);
    expect(screen.getByText("ADJACENT TRANSPOSITION GRAPH")).toBeDefined();
  });
});
