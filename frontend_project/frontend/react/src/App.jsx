import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from "react-router-dom";
import MainMenu from "./components/MainMenu";
import Home from "./pages/Home";
import Login from "./pages/Login";
import List from "./pages/List";
import Stock from "./pages/Stock";
import Setting from "./pages/Setting";


function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/stock" element={<Stock />} />
          <Route path="/list" element={<List />} />
          <Route path="/setting" element={<Setting />} />
          <Route path="/home" element={<Home />} />
          <Route path="/login" element={<Login />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;