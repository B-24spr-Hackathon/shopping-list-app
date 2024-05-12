import React, { useEffect } from "react";
import { Header, Footer } from "../components/HeaderImg";
import StockItems from "../components/StockItems";
import TabMainMenu from "../components/TabMainMenu";
import UserNameAndIcon from "../components/UserNameIcon";
import TabItems from "../components/TabItems";
import { AddBtn } from "../components/Buttons";
import { addNewListHandler } from "../components/TabItems";



function Items() {
    useEffect(() => {
        FetchUserInfo();
    }, [AddBtn]);

    return (
        <>

            <Header />
            <UserNameAndIcon />
            <TabMainMenu />
            <AddBtn children="+" onClick={addNewListHandler}/>

            <div className='flex justify-center mt-4'>

            <TabItems />
            </div>
            <Footer />


        </>

    );
}


export default Items;