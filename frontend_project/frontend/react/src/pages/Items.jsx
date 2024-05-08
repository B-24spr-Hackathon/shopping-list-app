import React from "react";
import { Header, Footer } from "../components/HeaderImg";
import StockItems from "../components/StockItems";
import TabMainMenu from "../components/TabMainMenu";
import UserNameAndIcon from "../components/UserNameIcon";
import TabItems from "../components/TabItems";

function Items() {

    return (
        <>

            <Header />
            <UserNameAndIcon />
            <TabMainMenu />
            <TabItems />
            <Footer />


        </>

    );
}


export default Items;