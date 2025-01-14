import "./App.css";
import FruitList from "./components/Fruits";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1 className="text-3xl underline">Fruit Management App</h1>
      </header>
      <main>
        <FruitList />
      </main>
    </div>
  );
}

export default App;
