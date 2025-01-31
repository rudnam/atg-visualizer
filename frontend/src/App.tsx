import "./App.css";
import "@mantine/core/styles.css";

import { generateColors } from "@mantine/colors-generator";
import { createTheme, MantineProvider } from "@mantine/core";
import Header from "./components/Header";
import Content from "./components/Content";

const theme = createTheme({
  fontFamily: "Inter, sans-serif",
  primaryColor: "maroon",
  colors: {
    maroon: generateColors("#7f1d1d"),
  },
});

function App() {
  return (
    <MantineProvider theme={theme}>
      <div className="App h-full flex flex-col">
        <Header />
        <main className="grow my-8">
          <Content />
        </main>
      </div>
    </MantineProvider>
  );
}

export default App;
