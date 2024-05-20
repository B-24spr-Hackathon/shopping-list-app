import React, { useEffect, useState } from "react";
import { useNavigate } from 'react-router-dom';
import { AddBtn, DeleteListBtn, LineBtn, TestBtn } from "../components/Buttons";
import { useSelector } from 'react-redux';
import { useCookies } from 'react-cookie';
import { applyToListRequest, approveToListRequest, deleteItemRequest, deleteListRequest, editListNameRequest, fetchItemsOfListRequest, fetchListInfoRequest, fetchMemberStatusInfoRequest, fetchShoppingListRequest, fetchUserInfoRequest, inviteToListRequest, searchApplyFriendRequest, searchFriendRequest, updateUserInfoRequest } from "../utils/Requests";
import { useDispatch } from "react-redux";
import { setUser, clearUser } from "../reducers/userSlice";
import { Footer, Header } from "../components/HeaderImg";
import { Title } from "../components/Title";
import { ForApplySelectList, ForInviteSelectList, SelectList } from "../components/SelectBox";
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
import lineLink from "../utils/LineLink";
import LineLinkBtn from "../utils/LineLink";
import DropUserBtn from "../utils/DropUser";
import MyListInfo from "../components/MyListInfo";

import { setMember } from "../reducers/memberSlice";
import MemberStatusModal from "../components/MemberStatusModal";



function Home() {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const user_id = useSelector((state) => state.user.user_id);
    const user_name = useSelector((state) => state.user.user_name);
    const userLineRemind = useSelector(state => state.user.remind);
    // const lists = useSelector(state => state.user.lists);
    const items = useSelector(state => state.items.items);
    const selectedList = useSelector(state => state.selectedList);
    const selectedListId = useSelector(state => state.selectedList.list_id);
    const handleAddNewList = AddNewList();

    const [cookies] = useCookies(['jwt_token']);
    const token = useSelector(state => state.token.token);
    const [lists, setLists] = useState([]);
    const [message, setMessage] = useState("");
    const [remind, setRemind] = useState(userLineRemind);
    const member = useSelector(state => state.member.member);
    const [memberInfo, setMemberInfo] = useState([]);

    
    //homeを読み込み時に実行
    useEffect(() => {
        const fetchUserInfo = async() => {
            //ユーザー情報取得
            const userInfo = await fetchUserInfoRequest(token);
            console.log('homeEffect');
            dispatch(setUser(userInfo.data.user));
            dispatch(setUser({lists:userInfo.data.lists}));
            const member_statusInfo = await fetchMemberStatusInfoRequest(token);
            console.log('status',member_statusInfo);
            dispatch(setMember(member_statusInfo.data));
            setMemberInfo(member_statusInfo.data);

            console.log('member:',member);
            console.log('memberInfo:',memberInfo);
            
            if (userInfo.data.lists.length == 0){
                setMessage("まだリストがありません");
                // await handleAddNewList();
            }else{
                setLists(userInfo.data.lists);
                await fetchListInfoRequest(selectedListId, token);
            }
        };
        fetchUserInfo();
    }, [selectedList]);


    const handleFetchShoppingList = async() => {
        const response = await fetchShoppingListRequest(selectedListId, token)
        console.log('fetchshopping:', response);
    }

    const handleDeleteList = async() => {
        const response = await deleteListRequest(selectedListId, token);
        const newUserInfo = await fetchUserInfoRequest(token);
            dispatch(setUser(newUserInfo.data.user));
            const lastIndex = newUserInfo.data.lists.length - 1;
            //selectedListのリスト情報を取得
            const listInfo = await fetchListInfoRequest(newUserInfo.data.lists[lastIndex].list_id, token);
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

    const [friendInviteUserId, setFriendInviteUserId] =useState();
    const [friendApplyUserId, setFriendApplyUserId] = useState()
    const [friendInviteUserInfo, setFriendInviteUserInfo] = useState({});
    const [friendApplyUserInfo, setFriendApplyUserInfo] = useState({});
    const [friendApplyUserLists, setFriendApplyUserLists] = useState([]);

    const handleSearchInviteFriend = async() => {
        try{
            const response = await searchFriendRequest(friendInviteUserId, token);
            setFriendInviteUserInfo(response.data);
            console.log('info',friendInviteUserInfo);
            console.log('lists',lists);

        }catch{
            console.log(err.response.data);
        }
    }
    const handleSearchApplyFriend = async() => {
        try{
            const response = await searchApplyFriendRequest(friendApplyUserId, token);
            setFriendApplyUserInfo(response.data);
            setFriendApplyUserLists(response.data.lists);
            console.log('friendApplyInfo',friendApplyUserInfo);
            console.log('friendApplylists',friendApplyUserLists);


        }catch{
            console.log(err.response.data);
        }
    }

    const [inviteAuthority, setInviteAuthority] = useState("False");
    const [applyAuthority, setApplyAuthority] = useState("False");

    const handleInviteFriendToList = async() => {
        try {
            const response = await inviteToListRequest( selectedInviteListId, friendInviteUserInfo.user_id, inviteAuthority, token);
        }catch{
            console.log(err.response.data);

        }
    }
    const handleApplyFriendToList = async() => {
        try {
            const response = await applyToListRequest( selectedApplyListId, user_id, applyAuthority, token);
        }catch{
            console.log(err.response.data);

        }
    }
    const [selectedInviteListId, setSelectedInviteListId] = useState();
    const handleSelectChange = (inviteListId) => {
        setSelectedInviteListId(inviteListId);
        console.log("Selected List ID:", inviteListId);
    }

    const [selectedApplyListId, setSelectedApplyListId] = useState([]);

    const handleApplyListSelectChange = (applyListId) => {
        setSelectedApplyListId(applyListId);
        console.log("Selected List ID:", applyListId);
    }

    const handleLineRemindChange = async() => {
        const newLineRemind = !userLineRemind;
        try {
            const response = await updateUserInfoRequest('remind', newLineRemind, token);
            dispatch(setUser({remind:response.data.user.remind}));
            setRemind(response.data.user.remind);

        }catch(err){
            console.error('Failed to update manage target:', err);
        }
    }



    const handleInviteAuthorityChange = (e) => {
        setInviteAuthority(e.target.value);
    };
    const handleApplyAuthorityChange = (e) => {
        setApplyAuthority(e.target.value);
    };

    const handleApproveToList = async(member_id) => {
        const response = await approveToListRequest(member_id, token);
        console.log('承認？',response);
    }

    return (
        <>
            <div className="flex flex-col">
                <Header />
                <div className="fixed right-2 mt-1 text-right">
                    <MemberStatusModal member={memberInfo} onApprove={handleApproveToList} />
                    <LogoutButton />
                </div>
                <div className="flex flex-col justify-center flex-grow items-center overflow-auto">
                    <Title children="ようこそ" />
                    <MyLists lists={lists} token={token} />
                    <p>{message}</p>

                    
                    
                    <AddBtn children="+" onClick={handleAddNewList} onChange={""} />


                    <TextInput type="text" placeholder="user_id" value={friendInviteUserId} onChange={e => setFriendInviteUserId(e.target.value)}/>
                    <TestBtn onClick={handleSearchInviteFriend} children='招待したい友達' />
                    <p>検索した友達ユーザー名{friendInviteUserInfo.user_name}</p>
                    <ForInviteSelectList lists={lists} onSelectChange={handleSelectChange} />
                    <PermissionDropdown value={inviteAuthority} onChange={handleInviteAuthorityChange} />
                    <TestBtn onClick={handleInviteFriendToList} children="招待"/>
                    <div>
                        <br />
                        <br />
                        

                    </div>
                    <TextInput type="text" placeholder="user_id" value={friendApplyUserId} onChange={e => setFriendApplyUserId(e.target.value)}/>
                    <TestBtn onClick={handleSearchApplyFriend} children='共有申請したい友達' />
                    <p>検索した友達ユーザー名{friendApplyUserInfo.user_name}</p>
                    <ForApplySelectList lists={friendApplyUserLists} onSelectChange={handleApplyListSelectChange} />
                    <PermissionDropdown value={applyAuthority} onChange={handleApplyAuthorityChange} />
                    <TestBtn onClick={handleApplyFriendToList} children="共有申請"/>
                    <br />
                    <TestBtn onClick={ () => navigate('/items')} children="itemsへ"/>
                    <TestBtn onClick={ () => navigate('/shoppinglist')} children="listへ"/>
                    <LineLinkBtn />
                    <div>
                        LINE通知ON or OFF
                    <input
                        type='checkbox'
                        checked={remind}
                        onChange={ () => handleLineRemindChange() }
                        />
                    </div>
                    <DropUserBtn />
                </div>
            </div>

        </>

    );
}


export default Home;