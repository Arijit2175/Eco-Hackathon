import React from "react";
import "./index.css";

import Header from "./components/Header";
import Dashboard from "./components/Dashboard";

function App() {
  return (
    <div className="app">
      <Header />
      <div className="container">
        <Dashboard />
      </div>
    </div>
  );
}

export default App;
