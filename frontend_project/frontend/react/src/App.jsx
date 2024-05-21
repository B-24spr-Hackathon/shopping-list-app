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
import Items from "./pages/Items";
import Setting from "./pages/Setting";
import Signup from "./pages/Signup";
import LineLoginError from "./pages/LineLoginError";
import ShoppingList from "./pages/ShoppingList";
import LineLoginForm from "./pages/LineLoginForm";
import ToDefault from "./pages/ToDefault";
import LineLoginMethod from "./utils/LineLoginMethod";
import LineLinkForm from "./pages/LineLinkForm";
import CombinedScreen from "./pages/Combined";


function App() {
  return (
    <Router>
      <AuthProvider>
        <div>
          <Routes>
            <Route exact path="/" element={<Login />} />
            <Route path="/items" element={<Items />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/shoppinglist" element={<ShoppingList />} />
            <Route path="/setting" element={<Setting />} />
            <Route path="/home" element={<Home />} />
            <Route path="/lineloginerror" element={<LineLoginError />} />
            <Route path="/lineloginform" element={<LineLoginForm />} />
            <Route path="/lineloginmethod" element={<LineLoginMethod />} />
            <Route path="/todefault" element={<ToDefault />} />
            <Route path="/linelinkform" element={<LineLinkForm/>} />
            <Route path="/comb" element={<CombinedScreen/>} />
            

          </Routes>
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;