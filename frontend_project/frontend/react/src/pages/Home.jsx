import React, { useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import { AddBtn, TestBtn } from "../components/Buttons";
import { useSelector } from 'react-redux';
import { useCookies } from 'react-cookie';
import { fetchShoppingListRequest, fetchUserInfoRequest } from "../utils/Requests";
import { useDispatch } from "react-redux";
import { setUser, clearUser } from "../reducers/userSlice";
import { Footer, Header } from "../components/HeaderImg";
import { Title } from "../components/Title";
import { SelectList } from "../components/SelectBox";
import AddNewList from "../utils/AddNewList";
import { setSelectedList } from "../reducers/selectedListSlice";
import LogoutButton from "../components/Logout";
import AddNewItem from "../utils/AddNewItem";

function Home() {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const user_id = useSelector((state) => state.user.user_id);
    const user_name = useSelector((state) => state.user.user_name);
    const lists = useSelector(state => state.user.lists);
    const items = useSelector(state => state.items.items);
    const selectedListId = useSelector(state => state.selectedList.list_id);
    const handleAddNewList = AddNewList();
    const handleAddNewItem = AddNewItem();
    const [cookies] = useCookies(['jwt_token']);

    useEffect(() => {
        const fetchUserInfo = async() => {
            const response = await fetchUserInfoRequest();
            dispatch(setUser(response.data.user))
            dispatch(setUser({lists:response.data.lists}));
            console.log(lists,lists.length);
            console.log(items,items.length);
            if (lists.length == 0){
                handleAddNewList();
            } else {
                dispatch(setSelectedList(lists[lists.length -1]));
            }

        };
        fetchUserInfo();
    }, []);

    const handleFetchUserInfo = async() => {
        try {
            const response = await fetchUserInfoRequest();
            console.log("fetch:",response);
            dispatch(setUser(response.data.user));
            dispatch(setUser({lists:response.data.lists}));
            console.log('lists:',lists.length);
            console.log('lists:',lists[0]);

            return response;
        }catch(err){
            // console.log(err.response.data);
            console.log("era-")
            console.log(err.response);
        };
    }

    const handleFetchShoppingList = async() => {
        const response = await fetchShoppingListRequest(4)
        console.log('fetchshopping:', response);
    }

    return (
        <>
            <div className="flex flex-col">
                <Header />
                <LogoutButton />
                <div className="flex flex-col justify-center flex-grow items-center overflow-auto">
                    <Title children="ようこそ" />
                    <SelectList />
                    <AddBtn children="+" onClick={handleAddNewList} />
                    <TestBtn onClick={ () => navigate('/items')} children="itemsへ"/>
                    <TestBtn onClick={ () => navigate('/shoppinglist')} children="listへ"/>
                    <TestBtn onClick={handleFetchUserInfo} children="get" />
                    <TestBtn children='test' onClick={handleFetchShoppingList}/>
                </div>
                <Footer />
            </div>

        </>

    );
}


export default Home;