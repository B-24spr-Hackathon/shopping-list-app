import React, { useState } from "react";
import { Tab, Tabs,TabList, TabPanel } from "react-tabs";
import '../styles/Tabs.css';


function TabItems({children}) {
    const [tabs, setTabs] = useState([
        {id: 1, title: "デフォルト", content: "Tab1 content"},
        {id: 2, title: "+", content: "Tab2 content"}
    ]);

    const [tabCount, setTabCount] = useState(3);

    const addTab = () => {
        const newTab = {
            id: tabCount,
            title: `Tab ${tabCount}`,
            content: `Tab ${tabCount} content`
        };
        setTabs([...tabs, newTab]);
        setTabCount(tabCount + 1);
    };

    const onTabSelect = (index) => {
        if(index === 1) {
            addTab();
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
    ]

    return (
        <>
            <Tabs onSelect={onTabSelect} className="items-tabs-container">
                <TabList className="items-tabs__tab-list">
                    {tabs.map(tab => (
                        <Tab key={tab.id} selectedClassName="items-tabs__tab--selected" className="items-tabs__tab">
                            {tab.title}
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

)};
export default TabItems;