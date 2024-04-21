import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from "react-router-dom";
import "../styles/MainMenu.css";

function MainMenu() {
    return (
        <>
        <div className="flex flex-col justify-center mt-12 pb-3 items-center w-full text-2xl border-b-2 border-gray">
            <nav>
            <ul className="flex space-x-40">
                <li className="px-2 "><Link to="/stock">在庫リスト</Link></li>
                <li className="px-2 "><Link to="/list">お買い物リスト</Link></li>
                <li className="px-2"><Link to="/setting">設定</Link></li>
                {/* <li><Link to="/home">HOME</Link></li> */}
                {/* <li><Link to="/login">ログアウト</Link></li> */}
            </ul>
            </nav>
        </div>
        </>
    );
  }
  export default MainMenu;