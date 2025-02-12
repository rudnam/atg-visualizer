import { generateColors } from "@mantine/colors-generator";
import { createTheme } from "@mantine/core";

const theme = createTheme({
  fontFamily: "Inter, sans-serif",
  primaryColor: "maroon",
  colors: {
    maroon: generateColors("#7f1d1d"),
  },
});

export default theme;
