import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from "react-router-dom";

function StockItems() {
    return (
        <>
        <div className="flex justify-center mt-12 pb-3 items-center w-full text-s">
            <div className="flex space-x-20">
                <div><input type="checkbox" checked="" onChange={""} /></div>
                <div>アタック</div>
                <div>3</div>
                <div>4週間</div>
                <div>2024/4/15</div>
                <div className="">+</div>
            </div>
            <div>
                <button className="bg-orange-400 hover:bg-orange-200 text-white font-bold py-2 px-4 rounded">開けた</button>
            </div>
        </div>
        </>
    );
  }
  export default StockItems;