import React, { useEffect, useState } from "react";
import { Header, Footer } from "../components/HeaderImg";
import { AddBtn, TestBtn, OrangeBtn } from "../components/Buttons";
import { fetchUserInfoRequest } from "../utils/Requests.jsx";
import { useDispatch, useSelector } from "react-redux";
import { ItemsListPanel, ShoppingListPanel } from "../components/ListPanels.jsx";
import { SelectList } from "../components/SelectBox.jsx";
import LogoutButton from "../components/Logout.jsx";
import { useNavigate } from "react-router-dom";
import SettingUserInfo from "../components/SettigUserInfo.jsx";
import UserNameAndIcon from "../components/UserNameIcon.jsx";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faHouse, faHouseCircleExclamation } from '@fortawesome/free-solid-svg-icons';
import ToHomeButton from "../components/ToHome.jsx";

function CombinedScreen() {
    const dispatch = useDispatch();
    const selectedList = useSelector(state => state.selectedList);
    const [lists, setLists] = useState([]);
    const token = useSelector(state => state.token.token);
    const navigate = useNavigate();
    const [selectedTab, setSelectedTab] = useState('items'); // タブの状態を管理
    const userInfo = useSelector(state => state.user);

    useEffect(() => {
        const fetchListAndItemsInfo = async () => {
            const listsOfUser = await fetchUserInfoRequest(token);
            setLists(listsOfUser.data.lists);
        };
        fetchListAndItemsInfo();
    }, []);

    const handleToHome = () => {
        navigate('/home');
    }

    return (
        <>
            <div className="flex flex-col">
                <Header />
                <div className="mt-3">
                        <UserNameAndIcon />
                </div>
                <div className="fixed flex right-2 mt-2 mr-4 z-40">
                    <ToHomeButton userInfo={userInfo} handleToHome={handleToHome} />
                    {/* <button onClick={handleToHome}>
                        <FontAwesomeIcon icon={faHouse}  style={{color: "#075ef2",fontSize:'32px'}} />
                    </button>
                    <button onClick={handleToHome}>
                        <FontAwesomeIcon icon={faHouseCircleExclamation} style={{color: "#ff6524",fontSize:'32px'}} />
                    </button> */}
                </div>
            <div className="flex justify-center mt-20">
                <button
                    className={`px-4 py-2 text-sm font-semibold ${selectedTab === 'items' ? 'text-orange-500 border-b-2 border-orange-500' : 'text-gray-600'}`}
                    onClick={() => setSelectedTab('items')}
                    >
                    管理商品
                </button>
                <button
                    className={`px-4 py-2 text-sm font-semibold ml-4 ${selectedTab === 'shopping' ? 'text-orange-500 border-b-2 border-orange-500' : 'text-gray-600'}`}
                    onClick={() => setSelectedTab('shopping')}
                    >
                    お買い物リスト
                </button>
                <button
                    className={`px-4 py-2 text-sm font-semibold ml-4 ${selectedTab === 'settings' ? 'text-orange-500 border-b-2 border-orange-500' : 'text-gray-600'}`}
                    onClick={() => setSelectedTab('settings')}
                    >
                    設定
                </button>
            </div>
            <div className="flex justify-center w-full items-center mt-8">
                <div className="">
                    <SelectList lists={lists} />
                </div>
            </div>
            <div className="mt-4">
                {selectedTab === 'items' && (
                    <div className="flex justify-center">
                        <div className='w-11/12'>
                            <ItemsListPanel />
                        </div>
                    </div>
                )}
                {selectedTab === 'shopping' && (
                    <div className="flex justify-center">
                        <div className='w-11/12'>
                            <ShoppingListPanel />
                        </div>
                    </div>
                )}
                {selectedTab === 'settings' && (
                    <div className="flex justify-center">
                        <div className='w-11/12'>
                            <SettingUserInfo />
                        </div>
                    </div>
                )}
            </div>

                </div>
        </>
    );
}

export default CombinedScreen;
