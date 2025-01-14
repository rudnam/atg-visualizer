import "./App.css";
import "@mantine/core/styles.css";

import { MantineProvider } from "@mantine/core";
import FruitList from "./components/Fruits";

function App() {
  return (
    <MantineProvider>
      <div className="App">
        <header className="App-header">
          <h1 className="text-4xl font-bold">Fruit Management App</h1>
        </header>
        <main>
          <FruitList />
        </main>
      </div>
    </MantineProvider>
  );
}

export default App;
