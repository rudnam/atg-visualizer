import { test, expect } from "@playwright/test";

test("has title", async ({ page }) => {
  await page.goto("./");

  await expect(page).toHaveTitle(/ATG Visualizer/);
});

test("renders atg when draw button is clicked", async ({ page }) => {
  await page.goto("./");

  const plotDiv = page.getByTestId("plot-container");

  await expect(plotDiv).toBeEmpty();

  await page.getByTestId("draw-button").click();

  await expect(plotDiv).not.toBeEmpty();
});

test("renders poset results when solve button is clicked", async ({ page }) => {
  await page.goto("./");

  const yTextarea = page.getByTestId("input-y");

  await expect(page.getByTestId("poset-result-component")).toHaveCount(0);

  await yTextarea.fill("1234\n4321");

  await page.getByTestId("solve-button").click();

  await expect(page.getByTestId("poset-result-component")).toHaveCount(2);
});
