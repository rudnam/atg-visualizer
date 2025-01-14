import "./App.css";
import "@mantine/core/styles.css";

import { createTheme, MantineProvider } from "@mantine/core";
import Header from "./components/Header";
import GraphComponent from "./components/Graph";
import InputForm from "./components/InputForm";

const theme = createTheme({
  fontFamily: "Inter, sans-serif",
});

function App() {
  return (
    <MantineProvider theme={theme}>
      <div className="App">
        <Header />
        <main className="mt-8 flex flex-col sm:flex-row justify-center gap-16">
          <InputForm />
          <GraphComponent />
        </main>
      </div>
    </MantineProvider>
  );
}

export default App;
