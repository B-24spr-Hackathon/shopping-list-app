import React, { useState, useRef, useEffect } from "react";
import { Tab, Tabs, TabList, TabPanel } from "react-tabs";
import '../styles/Tabs.css';
import axios from 'axios';

//デフォルト状態のタブ構成
function TabItems({ children }) {
    const [tabs, setTabs] = useState([
        { id: 0, title: "+", content: "", isEditing: false },
    ]);

    const [editingTitle, setEditingTitle] = useState("");

    //現在のtabの数を取得する
    const getNextTabId = () => {
        return tabs.length ? Math.max(...tabs.map(tab => tab.id)) + 1 : 1;
    }

    const addNewList = async() => {
        const jwtToken = document.cookie.split(';').find(row => row.startsWith('jwt_token')).split('=')[1];
        console.log(`JWT Token: ${jwtToken}`); // JWTトークンの確認

        if (!jwtToken) {
            console.log("jwt_tokenが見つかりません。");
            return;
        }

        const config = {
            headers: {
                'Content-Type': 'application/json',
                // 'Authorization': `Bearer ${jwtToken}`
            },
            withCredentials: true
        };

        const requestBody = JSON.stringify({ list_name: "新しい"});
        console.log(`Request Body: ${requestBody}`);
        console.log(`Headers: `, config.headers);

        try {
            const response = await axios.post('http://127.0.0.1:8000/api/list/', {list_name: "新しい"}, config);
            console.log("Response Data:", response.data);
            console.log("成功");
        } catch (err) {
            console.log("Request Failed:", err.response || err.message || err);
        }
    }

    //タブの追加
    const addTab = () => {
        //タブの数を取得して+1したものが新しいタブのIDとなる
        const newTabId = getNextTabId();
        const newTab = {
            id: newTabId,
            title: `新しいリスト${newTabId}`,
            content: "",
            isEditing: false
        };
        //IDが0ではないタブを取り出して、[それら、新しいタブ、ID=0のタブ]の順にstateに入れる
        setTabs(tabs => {
            const filteredTabs = tabs.filter(tab => tab.id !== 0);
            return [...filteredTabs, newTab, tabs.find(tab => tab.id === 0)];
        })
    };

    const onTabSelect = (index) => {
        // '+'タブが選択された場合にのみ新しいタブを追加
        console.log("Selected tab ID:", tabs[index].id, index);
        if (tabs[index].id === 0) {
            addNewList();
            addTab();
        }
    };

    // タブのダブルクリックイベント
    const handleDoubleClick = id => {
        setTabs(tabs.map(tab => tab.id === id ? { ...tab, isEditing: true } : tab));
        const currentTab = tabs.find(tab => tab.id === id);
        if (currentTab) setEditingTitle(currentTab.title);
    };

    // タイトル編集中の変更
    const handleChangeTitle = (e, id) => {
        setEditingTitle(e.target.value); // 入力中の値をステートに保存
    }

    const updateTabTitle = (id, newTitle) => {
        setTabs(tabs.map(tab => {
            if(tab.id === id) {
                return { ...tab, title: newTitle, isEditing: false };
            }
            return tab;
        }));
    };

    // キーイベントハンドラ
    const handleKeyPress = (e, id) => {
        if (e.key === 'Enter') {
            updateTabTitle(id, editingTitle);
            e.target.blur(); // 入力を終了し、フォーカスを外す
        }
    };

    // フォーカスが外れた時の処理
    const handleBlur = (id) => {
        updateTabTitle(id, editingTitle);
    };

    const itemsHeader = (
        <thead>
            <tr className="text-center">
                <th>管理する</th>
                <th>商品名</th>
                <th>消費サイクル</th>
                <th>直近の開封日</th>
                <th>サイトのリンク</th>
                <th>最終購入日</th>
                <th>通知する</th>
            </tr>
        </thead>
    );

    const itemsData = [
        { 管理: "管理内容1", 商品名: "商品1", 消費サイクル: "1ヶ月", 開封日: "2021-09-01", リンク: "http://example.com", 購入日: "2021-08-01", 通知: "はい" },
    ];

    return (
        <>
            <Tabs onSelect={onTabSelect} className="items-tabs-container">
                <TabList className="items-tabs__tab-list">
                    {tabs.map((tab, index) => (
                        <Tab key={tab.id} className="items-tabs__tab" selectedClassName="items-tabs__tab--selected" onDoubleClick={ () => handleDoubleClick(tab.id) }>
                            {tab.isEditing ? (
                                <input
                                    type="text"
                                    value={editingTitle}
                                    onChange={(e) => handleChangeTitle(e, tab.id)}
                                    onKeyDown={(e) => handleKeyPress(e, tab.id) }
                                    onBlur={(e) => handleBlur(tab.id)}
                                />
                            ) : (
                                <div>{tab.title}</div>
                            )}
                        </Tab>
                    ))}
                </TabList>
                {tabs.map(tab => (
                    <TabPanel key={tab.id} className="items-tabs__tab-panel" selectedClassName="items-tabs__tab-panel--selected">
                        {tab.content}
                        <table className="table-fixed w-full">
                            {itemsHeader}
                            <tbody>
                                {itemsData.map((item, index) => (
                                    <tr key={index} className="text-center">
                                        <td>{item.管理}</td>
                                        <td>{item.商品名}</td>
                                        <td>{item.消費サイクル}</td>
                                        <td>{item.開封日}</td>
                                        <td><a href={item.リンク} target="_blank" rel="noopener noreferrer">リンク</a></td>
                                        <td>{item.購入日}</td>
                                        <td>{item.通知}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                        <div>{children}</div>
                    </TabPanel>
                ))}
            </Tabs>
        </>
    );
}

export default TabItems;
