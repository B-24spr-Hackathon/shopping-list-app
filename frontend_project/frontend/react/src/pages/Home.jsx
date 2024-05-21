import React, { useEffect, useState } from "react";
import { useNavigate } from 'react-router-dom';
import { AddBtn, DeleteListBtn, LineBtn, OrangeBtn, TestBtn } from "../components/Buttons";
import { useSelector, useDispatch } from 'react-redux';
import { useCookies } from 'react-cookie';
import { applyToListRequest, approveToListRequest, declineToListRequest, deleteItemRequest, deleteListRequest, fetchItemsOfListRequest, fetchListInfoRequest, fetchMemberStatusInfoRequest, fetchShoppingListRequest, fetchUserInfoRequest, inviteToListRequest, searchApplyFriendRequest, searchFriendRequest, updateUserInfoRequest } from "../utils/Requests";
import { setUser, clearUser } from "../reducers/userSlice";
import { Footer, Header } from "../components/HeaderImg";
import { Title } from "../components/Title";
import { ForApplySelectList, ForInviteSelectList, SelectList } from "../components/SelectBox";
import AddNewList from "../utils/AddNewList";
import { setSelectedList } from "../reducers/selectedListSlice";
import LogoutButton from "../components/Logout";
import { TextInput, TextInput2 } from "../components/TextInput";
import { PermissionDropdown } from "../components/cmbSelectAuthority";
import LineLinkBtn from "../utils/LineLink";
import DropUserBtn from "../utils/DropUser";
import { setMember } from "../reducers/memberSlice";
import MemberStatusModal from "../components/MemberStatusModal";
import SelectMyList from "../components/SelectMyList";
import MyListInfoModal from "../components/MyListInfoModal";

function Home() {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const user_id = useSelector((state) => state.user.user_id);
    const user_name = useSelector((state) => state.user.user_name);
    const userLineRemind = useSelector(state => state.user.remind);
    const items = useSelector(state => state.items.items);
    const selectedList = useSelector(state => state.selectedList);
    const selectedListId = useSelector(state => state.selectedList.list_id);
    const handleAddNewList = AddNewList();
    const [cookies] = useCookies(['jwt_token']);
    const token = useSelector(state => state.token.token);
    const [list, setList] = useState();
    const lists = useSelector(state => state.user.lists);
    const [guest_info, setGuest_info] = useState([]);
    const [message, setMessage] = useState("");
    const [remind, setRemind] = useState(userLineRemind);
    const member = useSelector(state => state.member.member);
    const [memberInfo, setMemberInfo] = useState([]);
    const [selectedTab, setSelectedTab] = useState('invite'); // タブの状態を管理

    useEffect(() => {
        const fetchUserInfo = async () => {
            const userInfo = await fetchUserInfoRequest(token);
            dispatch(setUser(userInfo.data));
            if (userInfo.data.lists.length == 0) {
                setMessage('まだリストがありません');
            } else {
                dispatch(setSelectedList(userInfo.data.lists[0]))
                const response = await fetchListInfoRequest(selectedListId, token);
                setList(response.data);
                setGuest_info(response.data.guest_info);
            }
            const member_statusInfo = await fetchMemberStatusInfoRequest(token);
            dispatch(setMember(member_statusInfo.data));
            setMemberInfo(member_statusInfo.data);
            console.log('info', member);
        };
        fetchUserInfo();
    }, [selectedListId]);

    const handleFetchShoppingList = async () => {
        const response = await fetchShoppingListRequest(selectedListId, token);
        console.log('fetchshopping:', response);
    }

    const handleDeleteList = async () => {
        const response = await deleteListRequest(selectedListId, token);
        const newUserInfo = await fetchUserInfoRequest(token);
        dispatch(setUser(newUserInfo.data.user));
        const lastIndex = newUserInfo.data.lists.length - 1;
        const listInfo = await fetchListInfoRequest(newUserInfo.data.lists[lastIndex].list_id, token);
        dispatch(setSelectedList(listInfo.data));
    }

    const [friendInviteUserId, setFriendInviteUserId] = useState();
    const [friendApplyUserId, setFriendApplyUserId] = useState();
    const [friendInviteUserInfo, setFriendInviteUserInfo] = useState({});
    const [friendApplyUserInfo, setFriendApplyUserInfo] = useState({});
    const [friendApplyUserLists, setFriendApplyUserLists] = useState([]);

    const handleSearchInviteFriend = async () => {
        try {
            const response = await searchFriendRequest(friendInviteUserId, token);
            setFriendInviteUserInfo(response.data);
        } catch {
            console.log(err.response.data);
        }
    }

    const handleSearchApplyFriend = async () => {
        try {
            const response = await searchApplyFriendRequest(friendApplyUserId, token);
            setFriendApplyUserInfo(response.data);
            setFriendApplyUserLists(response.data.lists);
        } catch {
            console.log(err.response.data);
        }
    }

    const [inviteAuthority, setInviteAuthority] = useState("False");
    const [applyAuthority, setApplyAuthority] = useState("False");

    const handleInviteFriendToList = async () => {
        try {
            const response = await inviteToListRequest(selectedInviteListId, friendInviteUserInfo.user_id, inviteAuthority, token);
            const response1 = await fetchUserInfoRequest(token);
            dispatch(setUser(response1));
        } catch {
            console.log(err.response.data);
        }
    }

    const handleApplyFriendToList = async () => {
        try {
            const response = await applyToListRequest(selectedApplyListId, user_id, applyAuthority, token);
        } catch {
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

    const handleLineRemindChange = async () => {
        const newLineRemind = !userLineRemind;
        try {
            const response = await updateUserInfoRequest('remind', newLineRemind, token);
            dispatch(setUser({ remind: response.data.user.remind }));
            setRemind(response.data.user.remind);
        } catch (err) {
            console.error('Failed to update manage target:', err);
        }
    }

    const handleInviteAuthorityChange = (e) => {
        setInviteAuthority(e.target.value);
    };

    const handleApplyAuthorityChange = (e) => {
        setApplyAuthority(e.target.value);
    };

    const handleApproveToList = async (member_id) => {
        const response = await approveToListRequest(member_id, token);
        console.log('承認', response);
    }

    const handleDeclineToList = async (member_id) => {
        const response = await declineToListRequest(member_id, token);
        console.log('拒否OR中止', response);
    }

    return (
        <>
            <div className="flex flex-col">
                <Header />
                <div className="fixed right-2 mt-1 z-40">
                    <MemberStatusModal member={member} onApprove={handleApproveToList} onDecline={handleDeclineToList} />
                    <LogoutButton />
                </div>
                <div className="my-16">
                    <Title children="ようこそ" />
                </div>
                <div className="flex justify-center w-full items-center">
                    <div className="">
                        <SelectMyList lists={lists} />
                    </div>
                    <div className="ml-4">
                        <MyListInfoModal list={selectedList} guest_info={guest_info} />
                    </div>
                </div>
                <p>{message}</p>
                <div className="flex justify-center">
                    <div className="mx-1">
                        <OrangeBtn onClick={() => navigate('/items')} children="リストの商品を管理する" />
                    </div>
                    <div className="mx-1">
                        <OrangeBtn onClick={() => navigate('/shoppinglist')} children="お買い物リストを見る" />
                    </div>
                </div>
                <button onClick={handleAddNewList}>＋新しいリストを作成する</button>
                <div className="flex justify-center">
                    <div className="flex flex-col w-1/2 p-8">
                        <button onClick={() => setSelectedTab('invite')} className={`py-2 px-4 ${selectedTab === 'invite' ? 'bg-blue-500 text-white' : 'bg-white text-blue-500'}`}>友達を招待</button>
                        <button onClick={() => setSelectedTab('apply')} className={`py-2 px-4 ${selectedTab === 'apply' ? 'bg-blue-500 text-white' : 'bg-white text-blue-500'}`}>共有申請</button>
                    </div>
                </div>
                {selectedTab === 'invite' && (
                    <div className="flex justify-center">
                        <div className="flex flex-col w-1/2 p-8">
                            <div>
                                <TextInput2 type="text" placeholder="user_id" value={friendInviteUserId} onChange={e => setFriendInviteUserId(e.target.value)} />
                            </div>
                            <div>
                                <TestBtn onClick={handleSearchInviteFriend} children='招待したい友達' />
                            </div>
                            <div>
                                <p>検索した友達ユーザー名{friendInviteUserInfo.user_name}</p>
                            </div>
                            <div>
                                <ForInviteSelectList lists={lists} onSelectChange={handleSelectChange} />
                            </div>
                            <div>
                                <PermissionDropdown value={inviteAuthority} onChange={handleInviteAuthorityChange} />
                            </div>
                            <div>
                                <TestBtn onClick={handleInviteFriendToList} children="招待" />
                            </div>
                        </div>
                    </div>
                )}
                {selectedTab === 'apply' && (
                    <div className="flex justify-center">
                        <div className="flex flex-col w-1/2 p-8">
                            <div>
                                <TextInput2 type="text" placeholder="user_id" value={friendApplyUserId} onChange={e => setFriendApplyUserId(e.target.value)} />
                            </div>
                            <div>
                                <TestBtn onClick={handleSearchApplyFriend} children='共有申請したい友達' />
                            </div>
                            <div>
                                <p>検索した友達ユーザー名{friendApplyUserInfo.user_name}</p>
                            </div>
                            <div>
                                <ForApplySelectList lists={friendApplyUserLists} onSelectChange={handleApplyListSelectChange} />
                            </div>
                            <div>
                                <PermissionDropdown value={applyAuthority} onChange={handleApplyAuthorityChange} />
                            </div>
                            <div>
                                <TestBtn onClick={handleApplyFriendToList} children="共有申請" />
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </>
    );
}

export default Home;
