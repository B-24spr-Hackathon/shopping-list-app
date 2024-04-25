import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import List from "./pages/List";
import Items from "./pages/Items";
import Setting from "./pages/Setting";


function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route exact path="/" element={<Login />} />
          <Route path="/items" element={<Items />} />
          <Route path="/list" element={<List />} />
          <Route path="/setting" element={<Setting />} />
          <Route path="/home" element={<Home />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;