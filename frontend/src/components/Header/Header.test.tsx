import { describe, expect, test } from "vitest";
import { screen } from "@testing-library/react";
import { render } from "../../test-utils/render";
import Header from "./Header";

describe("Header", () => {
  test("renders", () => {
    render(<Header />);
    expect(screen.getByText("ATG Visualizer")).toBeDefined();
  });
});
