import React from "react";
import "./App.css";
import { AuthProvider } from "./utils/Auth";

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
import Signup from "./pages/Signup";


function App() {
  return (
    <Router>
      <AuthProvider>
        <div>
          <Routes>
            <Route exact path="/" element={<Login />} />
            <Route path="/items" element={<Items />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/list" element={<List />} />
            <Route path="/setting" element={<Setting />} />
            <Route path="/home" element={<Home />} />
          </Routes>
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;