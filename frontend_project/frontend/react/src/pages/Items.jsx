import React, { useEffect, useState } from "react";
import { Header, Footer } from "../components/HeaderImg";
import StockItems from "../components/StockItems";
import TabMainMenu from "../components/TabMainMenu";
import UserNameAndIcon from "../components/UserNameIcon";
import TabItems from "../components/TabItems";
import { AddBtn, TestBtn } from "../components/Buttons";
import { addNewListRequest, fetchListInfoRequest, fetchUserInfoRequest } from "../utils/Requests.jsx";
import { useDispatch, useSelector } from "react-redux";
import { setItemAllInfo } from "../reducers/itemSlice.jsx";
import { ItemsListPanel } from "../components/ListPanels.jsx";
import { SelectList } from "../components/SelectBox.jsx";
import LogoutButton from "../components/Logout.jsx";
import { useNavigate } from "react-router-dom";





function Items() {

    const dispatch = useDispatch();
    const selectedList = useSelector(state => state.selectedList);
    const [lists, setLists] = useState([]);
    const [items, setItems] = useState([]);
    const token = useSelector(state => state.token.token);
    const navigate = useNavigate();

   useEffect(() => {
    const fetchListAndItemsInfo = async() =>{
        const listsOfUser = await fetchUserInfoRequest(token);
        console.log('itemsEffectUser');
        setLists(listsOfUser.data.lists);
        // const itemsOfList = await fetchListInfoRequest(selectedList.list_id);
        // console.log('itemsEffectItemOfList',response);
        // setItems(itemsOfList.data.items);
    };
    fetchListAndItemsInfo();
   },[]);

   const handleToHome = () => {
    navigate('/home');
   }
    


    return (
        <>

            <Header />
            <div className="fixed right-2 mt-1 text-right">
                <LogoutButton />
                <TestBtn children='homeへ' onClick={handleToHome}/>
            </div>
            <UserNameAndIcon />
            <TabMainMenu />
            <div className="">

                <SelectList lists={lists}/>

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