import React, { useEffect, useState } from "react";
import { useNavigate } from 'react-router-dom';
import { AddBtn, DeleteListBtn, TestBtn } from "../components/Buttons";
import { useSelector } from 'react-redux';
import { useCookies } from 'react-cookie';
import { deleteItemRequest, deleteListRequest, editListNameRequest, fetchItemsOfListRequest, fetchListInfoRequest, fetchShoppingListRequest, fetchUserInfoRequest, inviteToListRequest, searchFriendRequest } from "../utils/Requests";
import { useDispatch } from "react-redux";
import { setUser, clearUser } from "../reducers/userSlice";
import { Footer, Header } from "../components/HeaderImg";
import { Title } from "../components/Title";
import { ForInviteSelectList, SelectList } from "../components/SelectBox";
import AddNewList from "../utils/AddNewList";
import { setSelectedList } from "../reducers/selectedListSlice";
import LogoutButton from "../components/Logout";
import AddNewItem from "../utils/AddNewItem";
import { setItemAllInfo } from "../reducers/itemSlice";
import { setShoppingItemsAllInfo } from "../reducers/shoppingItemsSlice";
import TextInput from "../components/TextInput";
import { EditableInput } from "../components/EditableDateInput";
import PermissionDropdown from "../components/cmbSelectAuthority";
import MyLists from "../components/MyLists";



function Home() {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const user_id = useSelector((state) => state.user.user_id);
    const user_name = useSelector((state) => state.user.user_name);
    // const lists = useSelector(state => state.user.lists);
    const items = useSelector(state => state.items.items);
    const selectedList = useSelector(state => state.selectedList);
    const selectedListId = useSelector(state => state.selectedList.list_id);
    const handleAddNewList = AddNewList();
    const handleAddNewItem = AddNewItem();
    const [cookies] = useCookies(['jwt_token']);
    const token = useSelector(state => state.token.token);
    const [lists, setLists] = useState([]);

    
    //homeを読み込み時に実行
    useEffect(() => {
        const fetchUserInfo = async() => {
            //ユーザー情報取得
            const userInfo = await fetchUserInfoRequest(token);
            // dispatch(setUser(userInfo.data.user));
            // dispatch(setUser({lists:userInfo.data.lists}));
            //リストがなければ、自動的にリストを一つ作成。あれば、最後のリストをselectedとする。
            if (userInfo.data.lists.length == 0){
                await handleAddNewList();
            } else {
                dispatch(setSelectedList(userInfo.data.lists[userInfo.data.lists.length -1]));
            }
            //改めてユーザー情報取得
            const newUserInfo = await fetchUserInfoRequest(token);
            setLists(newUserInfo.data.lists);
            const lastIndex = newUserInfo.data.lists.length - 1;
            //selectedListのリスト情報を取得
            const listInfo = await fetchListInfoRequest(newUserInfo.data.lists[lastIndex].list_id);
            dispatch(setSelectedList(listInfo.data));
            //該当リスト内のitem情報を取得
            // const itemsInfo = await fetchItemsOfListRequest(listInfo.data.list_id);
            // dispatch(setItemAllInfo(itemsInfo.data.items));
            //該当リストの買い物リストを取得
            // const shoppingListInfo = await fetchShoppingListRequest(listInfo.data.list_id);
            // dispatch(setShoppingItemsAllInfo(shoppingListInfo.data));
            console.log('token',token);

        };
        fetchUserInfo();
    }, []);

    // const handleFetchUserInfo = async() => {
    //     try {
    //         const response = await fetchUserInfoRequest();
    //         console.log("fetch:",response);
    //         dispatch(setUser(response.data.user));
    //         dispatch(setUser({lists:response.data.lists}));
    //         console.log('lists:',lists.length);
    //         console.log('lists:',lists[0]);

    //         return response;
    //     }catch(err){
    //         // console.log(err.response.data);
    //         console.log("era-")
    //         console.log(err.response);
    //     };
    // }

    const handleFetchShoppingList = async() => {
        const response = await fetchShoppingListRequest(selectedListId)
        console.log('fetchshopping:', response);
    }

    const handleDeleteList = async() => {
        const response = await deleteListRequest(selectedListId, token);
        const newUserInfo = await fetchUserInfoRequest(token);
            dispatch(setUser(newUserInfo.data.user));
            const lastIndex = newUserInfo.data.lists.length - 1;
            //selectedListのリスト情報を取得
            const listInfo = await fetchListInfoRequest(newUserInfo.data.lists[lastIndex].list_id);
            dispatch(setSelectedList(listInfo.data));
            //該当リスト内のitem情報を取得
            // const itemsInfo = await fetchItemsOfListRequest(listInfo.data.list_id);
            // dispatch(setItemAllInfo(itemsInfo.data.items));
            //該当リストの買い物リストを取得
            // const shoppingListInfo = await fetchShoppingListRequest(listInfo.data.list_id);
            // dispatch(setShoppingItemsAllInfo(shoppingListInfo.data));

    }

    const handleEditListName = async(newValue) => {
        const response = await editListNameRequest(selectedList.list_id, newValue, token);
        dispatch(setSelectedList({...selectedList, list_name:newValue}));
    }

    const [friendUserId, setFriendUserId] =useState();
    const [friendUserInfo, setFriendUserInfo] = useState({});

    const handleSearchFriend = async() => {
        try{
            const response = await searchFriendRequest(friendUserId, token);
            setFriendUserInfo(response.data);
            console.log('info',friendUserInfo);

        }catch{
            console.log(err.response.data);
        }
    }

    const [authority, setAuthority] = useState("False");

    const handleInviteFriendToList = async() => {
        try {
            const response = await inviteToListRequest( selectedList.list_id, friendUserInfo.user_id, authority, token);
        }catch{
            console.log(err.response.data);

        }
    }

    const handleSelectChange = (listId) => {
        setSelectedListId(listId);
        console.log("Selected List ID:", listId);
    }



    const handleAuthorityChange = (e) => {
        setAuthority(e.target.value);
    };

    return (
        <>
            <div className="flex flex-col">
                <Header />
                <div className="fixed right-2 mt-1 text-right">
                    <LogoutButton />
                </div>
                <div className="flex flex-col justify-center flex-grow items-center overflow-auto">
                    <Title children="ようこそ" />
                    <MyLists lists={lists} />
                    
                    
                    <AddBtn children="+" onClick={handleAddNewList} onChange={""} />
                    <TextInput type="text" placeholder="user_id" value={friendUserId} onChange={e => setFriendUserId(e.target.value)}/>
                    <ForInviteSelectList onSelectChange={handleSelectChange} />
                    <p>検索した友達ユーザー名{friendUserInfo.user_name}</p>
                    <TestBtn onClick={handleSearchFriend} children='友達検索' />
                    <PermissionDropdown value={authority} onChange={handleAuthorityChange} />
                    <TestBtn onClick={handleInviteFriendToList} children="招待"/>
                    <TestBtn onClick={ () => navigate('/items')} children="itemsへ"/>
                    <TestBtn onClick={ () => navigate('/shoppinglist')} children="listへ"/>

                </div>
                <Footer />
            </div>

        </>

    );
}


export default Home;