import React, { useEffect, useState } from "react";
import { Header, Footer } from "../components/HeaderImg";
import StockItems from "../components/StockItems";
import TabMainMenu from "../components/TabMainMenu";
import UserNameAndIcon from "../components/UserNameIcon";
import TabItems from "../components/TabItems";
import { AddBtn, TestBtn } from "../components/Buttons";
import { addNewListRequest, fetchListInfoRequest } from "../utils/Requests.jsx";
import { useDispatch, useSelector } from "react-redux";
import { setItemAllInfo } from "../reducers/itemSlice.jsx";
import { ItemsListPanel } from "../components/ListPanels.jsx";
import { SelectList } from "../components/SelectBox.jsx";
import LogoutButton from "../components/Logout.jsx";





function Items() {

    const dispatch = useDispatch();
    const selectedList = useSelector(state => state.selectedList);
    const [lists, setLists] = useState([]);

   useEffect(() => {
    const fetchListAndItemsInfo = async() =>{
        const response = await fetchListInfoRequest(selectedList.list_id);
        setLists(response.data.lists);
        
    };
    fetchListAndItemsInfo();
   },[]);


    


    return (
        <>

            <Header />
            <div className="fixed right-2 mt-1 text-right">
                <LogoutButton />
            </div>
            <UserNameAndIcon />
            <TabMainMenu />
            <div className="">

                <SelectList />

                <div className='flex justify-center '>

                    <ItemsListPanel />
                </div>
            </div>

            <footer>aaa</footer>
            {/* <Footer /> */}


        </>

    );
}


export default Items;