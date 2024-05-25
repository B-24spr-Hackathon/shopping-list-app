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
import LoginNew from "./pages/LoginNew";


function App() {
  return (
    <Router>
      <AuthProvider>
        <div>
          <Routes>
            <Route exact path="/" element={<LoginNew />} />
            <Route path="/shoppinglist" element={<CombinedScreen/>} />
            <Route path="/home" element={<Home />} />
            <Route path="/lineloginerror" element={<LineLoginError />} />
            <Route path="/lineloginform" element={<LineLoginForm />} />
            <Route path="/lineloginmethod" element={<LineLoginMethod />} />
            <Route path="/todefault" element={<ToDefault />} />
            <Route path="/linelinkform" element={<LineLinkForm/>} />

            <Route path="/itemsold" element={<Items />} />
            <Route path="/settingold" element={<Setting />} />
            <Route path="/signupold" element={<Signup />} />
            <Route path="/oldshopping" element={<ShoppingList />} />
            <Route path="/oldlogin" element={<Login/>} />

            

          </Routes>
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;