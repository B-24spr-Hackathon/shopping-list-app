import React from "react";
import MainMenu from "../components/MainMenu";
import { Header, Footer } from "../components/HeaderImg";
import StockItems from "../components/StockItems";

function Items() {
    return (
        <>
            <Header />
            <MainMenu />
            <div className="flex justify-center mt-12 pb-3 items-center w-full text-s">
                <div className="flex space-x-20">
                    <div>通知</div>
                    <div>品名</div>
                    <div>現在数</div>
                    <div>サイクル</div>
                    <div>直近の開封日</div>
                    <div>サイトのリンク</div>
                </div>
            </div>
            <div className="flex justify-center w-full">
                <div className="border-b-2 border-gray w-3/4"></div>
            </div>
            <div>
                {Array.from({ length:3 }, (_, index) =>(
                    <StockItems key={index} />
                ))}
            </div>
            <Footer />





        </>

    );
}


export default Items;