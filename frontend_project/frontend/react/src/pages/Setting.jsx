import React from "react";
import { Header, Footer } from "../components/HeaderImg";
import StockItems from "../components/StockItems";
import TabMainMenu from "../components/TabMainMenu";

function Setting() {
    return (
        <>
            <div className="flex flex-col min-h-screen">
                <Header />
                <TabMainMenu />

                <div className="flex flex-col justify-center items-center overflow-auto mb-1">
                    <div className="flex space-x-20">
                        <div>
                            設定画面
                        </div>
                    </div>
                </div>
                <Footer />
            </div>





        </>

    );
}

export default Setting;