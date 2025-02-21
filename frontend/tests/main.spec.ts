import { test, expect } from "@playwright/test";

test("has title", async ({ page }) => {
  await page.goto("./");

  await expect(page).toHaveTitle(/ATG Visualizer/);
});

test("renders atg when draw button is clicked", async ({ page }) => {
  await page.goto("./");

  const plotDiv = page.getByTestId("plot-div");

  await expect(plotDiv).toBeEmpty();

  await page.getByTestId("draw-button").click();

  await expect(plotDiv).not.toBeEmpty();
});
