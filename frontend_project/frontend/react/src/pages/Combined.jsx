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

function CombinedScreen() {
    const dispatch = useDispatch();
    const selectedList = useSelector(state => state.selectedList);
    const [lists, setLists] = useState([]);
    const token = useSelector(state => state.token.token);
    const navigate = useNavigate();
    const [selectedTab, setSelectedTab] = useState('items'); // タブの状態を管理

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
            <Header />
            <div className="fixed right-2 mt-1 text-right">
                <LogoutButton />
                <TestBtn children='homeへ' onClick={handleToHome} />
            </div>
            <div className="flex justify-center w-full items-center">
                <div className="">
                    <SelectList lists={lists} />
                </div>
            </div>
            <div className="flex justify-center mt-8">
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

        </>
    );
}

export default CombinedScreen;
