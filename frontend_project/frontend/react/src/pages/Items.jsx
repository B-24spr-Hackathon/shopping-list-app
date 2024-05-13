import React, { useState } from "react";
import { Header, Footer } from "../components/HeaderImg";
import StockItems from "../components/StockItems";
import TabMainMenu from "../components/TabMainMenu";
import UserNameAndIcon from "../components/UserNameIcon";
import TabItems from "../components/TabItems";
import { AddBtn } from "../components/Buttons";
import { addNewListRequest } from "../utils/Requests.jsx";
import { useDispatch } from "react-redux";
import { setItemAllInfo, clearItem } from "../reducers/itemSlice.jsx";
import { ItemsListPanel } from "../components/ListPanels.jsx";
import { SelectList } from "../components/SelectBox.jsx";




function Items() {

    const dispatch = useDispatch();


    const handleAddNewList = async() => {
        try {
            const data = await addNewListRequest();
            console.log("newList",data.data);
            // dispatch(setItem(data.data))
        } catch(err) {
        console.log(err.response.data);
        };
    }
    // useEffect(() => {
    //     const fetchUserInfo = async() => {
    //         const data = await FetchUserInfoRequest();
    //     };
    //     fetchUserInfo();
    // }, []);


    return (
        <>

            <Header />
            <UserNameAndIcon />
            <TabMainMenu />
            <AddBtn children="+" onClick={handleAddNewList}/>
            <SelectList />

            <div className='flex justify-center mt-4'>

            <ItemsListPanel />
            </div>
            <Footer />


        </>

    );
}


export default Items;