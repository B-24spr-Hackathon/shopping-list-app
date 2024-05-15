import React, { useState, useRef, useEffect } from "react";
import { Tab, Tabs, TabList, TabPanel } from "react-tabs";
import '../styles/Tabs.css';
import { addNewListRequest } from "../utils/Requests";
import { useSelector } from "react-redux";


function TabItems({ children }) {
    const listTitle = useSelector((state) => state.user.lists[0].list_name);
    const [tabs, setTabs] = useState([
        { id: 0, title: "+", content: "", isEditing: false },
    ]);

    const [editingTitle, setEditingTitle] = useState("");

    //現在のtabの数を取得する
    const getNextTabId = () => {
        return tabs.length ? Math.max(...tabs.map(tab => tab.id)) + 1 : 1;
    }


    

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
                <th>   </th>
                <th>通知する</th>
            </tr>
        </thead>
    );

    const itemsData = [
        { 管理: "", 商品名: "商品1", 消費サイクル: "1ヶ月", 開封日: "2021-09-01", リンク: "http://example.com", 購入日: "2021-08-01", 通知: "はい" },
    ];


    
    return (
        <>
            <div className='item-field-container'>
                <div className="item-field-title">
                    MyHome
                </div>
                <div className="item-field">
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
                                    <td>ボタン</td>
                                    <td>{item.通知}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
            {/* <Tabs onSelect={onTabSelect} className="items-tabs-container">
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
            </Tabs> */}
        </>
    );
}

export default TabItems;
