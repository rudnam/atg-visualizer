import "./App.css";
import "@mantine/core/styles.css";

import { generateColors } from "@mantine/colors-generator";
import { createTheme, MantineProvider } from "@mantine/core";
import Header from "./components/Header";
import InputForm from "./components/InputForm";

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
        <main className="px-4 md:px-8 mt-8 grow flex flex-col sm:flex-row justify-center gap-12 w-full max-w-6xl mx-auto">
          <InputForm />
        </main>
      </div>
    </MantineProvider>
  );
}

export default App;
