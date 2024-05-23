import React, { useEffect, useState } from "react";
import { useNavigate } from 'react-router-dom';
import { AddBtn, DeleteListBtn, LineBtn, OrangeBtn, TestBtn } from "../components/Buttons";
import { useSelector, useDispatch } from 'react-redux';
import { useCookies } from 'react-cookie';
import { applyToListRequest, approveToListRequest, declineToListRequest, deleteItemRequest, deleteListRequest, fetchItemsOfListRequest, fetchListInfoRequest, fetchMemberStatusInfoRequest, fetchShoppingListRequest, fetchUserInfoRequest, inviteToListRequest, searchApplyFriendRequest, searchFriendRequest, updateUserInfoRequest } from "../utils/Requests";
import { setUser, clearUser } from "../reducers/userSlice";
import { Footer, Header } from "../components/HeaderImg";
import { Bar, Title } from "../components/Title";
import { ForApplySelectList, ForInviteSelectList, SelectList } from "../components/SelectBox";
import AddNewList from "../components/AddNewList";
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
import { UserNameAndIcon, OtherUserNameAndIcon } from "../components/UserNameIcon";
import SimpleSelectBox from "../components/SimpleReactSelect";
import HamburgerMenu from "../components/HumbergerMenu";



function Home() {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const token = useSelector(state => state.token.token);
    const user_id = useSelector((state) => state.user.user_id);
    const selectedList = useSelector(state => state.selectedList);
    const member = useSelector(state => state.member.member);
    const lists = useSelector(state => state.user.lists);


    const [message, setMessage] = useState("");
    const [selectedTab, setSelectedTab] = useState('invite'); // タブの状態を管理

    useEffect(() => {
        const fetchUserInfo = async () => {
            if (lists.length == 0) {
                setMessage('まだリストがありません');
            } else {

                //dispatch(setSelectedList(userInfo.data.lists[0]))
                // const response = await fetchListInfoRequest(selectedListId, token);
                // setList(response.data);
                // setGuest_info(response.data.guest_info);
            }
        };
        fetchUserInfo();
    }, []);

    // const handleFetchShoppingList = async () => {
    //     const response = await fetchShoppingListRequest(selectedListId, token);
    //     console.log('fetchshopping:', response);
    // }

    // const handleDeleteList = async () => {
    //     const response = await deleteListRequest(selectedListId, token);
    //     const newUserInfo = await fetchUserInfoRequest(token);
    //     dispatch(setUser(newUserInfo.data.user));
    //     const lastIndex = newUserInfo.data.lists.length - 1;
    //     const listInfo = await fetchListInfoRequest(newUserInfo.data.lists[lastIndex].list_id, token);
    //     dispatch(setSelectedList(listInfo.data));
    // }
    
    //招待と申請
    const [friendInviteUserId, setFriendInviteUserId] = useState();
    const [friendApplyUserId, setFriendApplyUserId] = useState();
    const [friendInviteUserInfo, setFriendInviteUserInfo] = useState({});
    const [friendApplyUserInfo, setFriendApplyUserInfo] = useState({});
    const [friendApplyUserLists, setFriendApplyUserLists] = useState([]);
    const [inviteAuthority, setInviteAuthority] = useState("False");
    const [applyAuthority, setApplyAuthority] = useState("False");

    //招待する友達を検索
    const handleSearchInviteFriend = async () => {
        try {
            const response = await searchFriendRequest(friendInviteUserId, token);
            setFriendInviteUserInfo(response.data);
        } catch {
            console.log(err.response.data);
        }
    }
    //申請する友達を検索
    const handleSearchApplyFriend = async () => {
        try {
            const response = await searchApplyFriendRequest(friendApplyUserId, token);
            setFriendApplyUserInfo(response.data);
            setFriendApplyUserLists(response.data.lists);
        } catch {
            console.log(err.response.data);
        }
    }
    //招待する
    const handleInviteFriendToList = async () => {
        try {
            const inviteResponse = await inviteToListRequest(selectedInviteListId, friendInviteUserInfo.user_id, inviteAuthority, token);
            const userInfoResponse = await fetchUserInfoRequest(token);
            dispatch(setUser(userInfoResponse.data.user));
            const memberStatusInfoResponse = await fetchMemberStatusInfoRequest(token);
            dispatch(setMember(memberStatusInfoResponse.data));
            console.log("招待",inviteResponse);
        } catch {
            console.log(err.inviteResponse.data);
        }
    }
    //申請する
    const handleApplyFriendToList = async () => {
        try {
            const response = await applyToListRequest(selectedApplyListId, user_id, applyAuthority, token);
            const userInfoResponse = await fetchUserInfoRequest(token);
            dispatch(setUser(userInfoResponse.data.user));
            const memberStatusInfoResponse = await fetchMemberStatusInfoRequest(token);
            dispatch(setMember(memberStatusInfoResponse.data));
            console.log("申請",response);
        } catch {
            console.log(err.response.data);
        }
    }
    //招待する自分のリストを選ぶ
    const [selectedInviteListId, setSelectedInviteListId] = useState();
    const handleSelectChange = (inviteListId) => {
        setSelectedInviteListId(inviteListId);
        console.log("Selected List ID:", inviteListId);
    }
    //申請する友達のリストを選ぶ
    const [selectedApplyListId, setSelectedApplyListId] = useState([]);
    const handleApplyListSelectChange = (applyListId) => {
        setSelectedApplyListId(applyListId);
        console.log("Selected List ID:", applyListId);
    }
    //申請する友達の権限を設定する
    const handleInviteAuthorityChange = (e) => {
        setInviteAuthority(e.target.value);
    };
    //招待する友達の権限を選ぶ
    const handleApplyAuthorityChange = (e) => {
        setApplyAuthority(e.target.value);
    };
    //承認する
    const handleApproveToList = async (member_id) => {
        const response = await approveToListRequest(member_id, token);
        const userInfoResponse = await fetchUserInfoRequest(token);
        dispatch(setUser(userInfoResponse.data.user));
        const memberStatusInfoResponse = await fetchMemberStatusInfoRequest(token);
        dispatch(setMember(memberStatusInfoResponse.data));
        console.log('承認', response);
    }
    //拒否・中止する
    const handleDeclineToList = async (member_id) => {
        const response = await declineToListRequest(member_id, token);
        const userInfoResponse = await fetchUserInfoRequest(token);
        dispatch(setUser(userInfoResponse.data.user));
        const memberStatusInfoResponse = await fetchMemberStatusInfoRequest(token);
        dispatch(setMember(memberStatusInfoResponse.data));
        console.log('拒否OR中止', response);
    }

    return (
        <>
            <div className="flex flex-col">
                <Header />
                <div className="mt-3">
                    <UserNameAndIcon />
                </div>
                <div className="fixed flex right-2 mt-1 mr-4 z-40">
                    <div className="">
                        <HamburgerMenu member={member} onApprove={handleApproveToList} onDecline={handleDeclineToList}/>
                    </div>
                </div>
                <div className="flex justify-center my-2">

                    <img className="w-52 h-40 object-cover rounded-full" src="/kaimotto.jpeg"/>
                </div>
                <div className="text-center text-lg mt-2 mb-8 font-sans">
                    <Bar children='もっと上手にまとめ買い！無駄なく、もれなく、買いもっと！' />
                </div>
                <div className="flex mb-2 justify-center w-full items-center">
                    <div className="w-1/2 max-w-64">
                        <SelectList lists={lists} />
                    </div>
                    {/* リスト情報モーダル */}
                    <div className="ml-4">
                        <MyListInfoModal />
                    </div>
                </div>
                    <div className="flex justify-center">
                        {message}
                    </div>
                    <AddNewList />
                <div className="flex justify-center ">
                    <div className="my-4">
                        <OrangeBtn disabled={lists.length == 0} onClick={() => navigate('/shoppinglist')} children="選んだリストを見る" />
                    </div>
                    {/* <div className="mx-1">
                        <OrangeBtn onClick={() => navigate('/comb')} children="お買い物リストを見る" />
                    </div> */}
                </div>
                <div className="flex justify-center">
                    <div className="flex flex-col w-auto p-4">
                        <button onClick={() => setSelectedTab('invite')} className={`py-2 px-4 rounded-t-lg border ${selectedTab === 'invite' ? 'bg-blue-500 text-white' : 'bg-white text-blue-500'}`}>友達を招待</button>
                        <button onClick={() => setSelectedTab('apply')} className={`py-2 px-4 rounded-b-lg ${selectedTab === 'apply' ? 'bg-blue-500 text-white' : 'bg-white text-blue-500'}`}>共有を申請</button>
                    </div>
                </div>
                {selectedTab === 'invite' && (
                    <div className="flex justify-center">
                        <div className="flex flex-col w-1/2 p-8 ">
                            <div className="flex justify-center w-full mb-2">
                                <TextInput2 type="text" placeholder="ユーザーID" value={friendInviteUserId} onChange={e => setFriendInviteUserId(e.target.value)} />
                            </div>
                            <div className="flex justify-center w-full mb-2">
                                <TestBtn onClick={handleSearchInviteFriend} children='友達検索' />
                            </div>
                            <div className="flex flex-row justify-center w-auto mb-2">
                                <div className="flex items-center">
                                    検索結果：
                                </div>
                                <div className="flex justify-center">
                                    <OtherUserNameAndIcon userInfo={friendInviteUserInfo.user_name} />
                                </div>
                            </div>
                            <div className="flex justify-center w-full mb-2">
                                <ForInviteSelectList lists={lists} onSelectChange={handleSelectChange} />
                            </div>
                            <div className="flex justify-center w-full mb-2">
                                <PermissionDropdown value={inviteAuthority} onChange={handleInviteAuthorityChange} />
                            </div>
                            <div className="flex justify-center w-full mb-2">
                                <TestBtn onClick={handleInviteFriendToList} children="招待" />
                            </div>
                        </div>
                    </div>
                )}
                {selectedTab === 'apply' && (
                    <div className="flex justify-center">
                        <div className="flex flex-col justify-center w-1/2 p-8 ">
                            <div className="flex justify-center w-full mb-2">
                                <TextInput2 type="text" placeholder="ユーザーID" value={friendApplyUserId} onChange={e => setFriendApplyUserId(e.target.value)} />
                            </div>
                            <div className="flex justify-center w-full mb-2">
                                <TestBtn onClick={handleSearchApplyFriend} children='友達検索' />
                            </div>
                            <div className="flex flex-row justify-center w-auto mb-2">
                                <div className="flex items-center">
                                    検索結果：
                                </div>
                                <div className="flex justify-center">
                                    <OtherUserNameAndIcon userInfo={friendApplyUserInfo.user_name} />
                                </div>
                            </div>
                            <div className="flex justify-center w-full mb-2">
                                <ForApplySelectList lists={friendApplyUserLists} onSelectChange={handleApplyListSelectChange} />
                            </div>
                            <div className="flex justify-center w-full mb-2">
                                <PermissionDropdown value={applyAuthority} onChange={handleApplyAuthorityChange} />
                            </div>
                            <div className="flex justify-center w-full mb-2">
                                <TestBtn onClick={handleApplyFriendToList} children="申請" />
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </>
    );
}

export default Home;
