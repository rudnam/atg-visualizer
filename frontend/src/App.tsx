import "./App.css";
import "@mantine/core/styles.css";

import { MantineProvider } from "@mantine/core";
import Header from "./components/Header/Header";
import Content from "./components/Content/Content";
import theme from "./theme";

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
