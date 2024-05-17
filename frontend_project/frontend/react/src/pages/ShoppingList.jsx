import React, { useEffect, useState } from 'react';
import TabMainMenu from "../components/TabMainMenu";
import { Header, Footer } from "../components/HeaderImg";
import UserNameAndIcon from '../components/UserNameIcon';
import { ShoppingListPanel } from '../components/ListPanels';
import LogoutButton from '../components/Logout';
import { SelectList } from '../components/SelectBox';
import { useSelector } from 'react-redux';
import { fetchUserInfoRequest } from '../utils/Requests';


function ShoppingList() {


    const selectedList = useSelector(state => state.selectedList);
    const [lists, setLists] = useState([]);
    const [items, setItems] = useState([]);
    const token = useSelector(state => state.token.token);
    useEffect(() => {
        const fetchListAndItemsInfo = async() =>{
            const listsOfUser = await fetchUserInfoRequest(token);
            console.log('shoppingEffectUser');
            setLists(listsOfUser.data.lists);
            // const itemsOfList = await fetchListInfoRequest(selectedList.list_id);
            // console.log('itemsEffectItemOfList',response);
            // setItems(itemsOfList.data.items);
        };
        fetchListAndItemsInfo();
       },[]);
    
    
    return (
        <>
            <Header />
            <LogoutButton />
            <UserNameAndIcon />


                <TabMainMenu />
                <SelectList lists={lists}/>
                <div className='flex justify-center mt-4'>

                <ShoppingListPanel />
                </div>
            <Footer />
        </>

    );
}


export default ShoppingList;