import React, { useState } from "react";
import { Tab, Tabs, TabList, TabPanel } from "react-tabs";
import '../styles/Tabs.css';

//デフォルト状態のタブ構成
function TabItems({ children }) {
    const [tabs, setTabs] = useState([
        { id: 1, title: "デフォルト", content: "", isEditing: false },
        { id: 0, title: "+", content: "", isEditing: false },
    ]);
    //現在のtabの数を取得する
    const findTabMaxId = () => {
        const maxId = tabs.reduce((max, tab) => tab.id !== 0 ? Math.max(max, tab.id) : max, 0);
        return maxId;
    };
    //タブの追加
    const addTab = () => {
        //タブの数を取得して+1したものが新しいタブのIDとなる
        const newTabId = findTabMaxId() + 1;
        const newTab = {
            id: newTabId,
            title: "",
            content: "",
            isEditing: true
        };
        //IDが0ではないタブを取り出して、[それら、新しいタブ、ID=0のタブ]の順にstateに入れる
        setTabs(tabs => {
            const filteredTabs = tabs.filter(tab => tab.id !== 0);
            return [...filteredTabs, newTab, tabs.find(tab => tab.id === 0)];
        })
        setTabCount(tabCount + 1);
    };

    const onTabSelect = (index) => {
        // '+'タブが選択された場合にのみ新しいタブを追加
        if (tabs[index].title === "+") {
            addTab();
        }
    };

    const handleDoubleClick = (id) => {
        // タブのタイトルをダブルクリックすると編集可能に
        setTabs(tabs.map(tab => {
            if (tab.id === id) return { ...tab, isEditing: true };
            return tab;
        }));
    };

    const handleTitleChange = (id, title) => {
        setTabs(tabs.map(tab => {
            if (tab.id === id) return { ...tab, title, isEditing: false };
            return tab;
        }));
    };
    const handleKeyPress = (e, id) => {
        if (e.key === 'Enter') {
            handleTitleChange(id, e.target.value);
        }
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
                    {tabs.map((tab) => (
                        <Tab key={tab.id} className="items-tabs__tab" selectedClassName="items-tabs__tab--selected">
                            {tab.isEditing ? (
                                <input
                                    type="text"
                                    value={tab.title}
                                    onBlur={() => handleTitleChange(tab.id, tab.title, true)}
                                    onChange={(e) => handleTitleChange(tab.id, e.target.value)}
                                    onKeyDown={(e) => handleKeyPress(e,tab.id)}
                                    autoFocus
                                />
                            ) : (
                                <div onDoubleClick={() => handleDoubleClick(tab.id)}>{tab.title}</div>
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
