import React from "react";
import { useNavigate } from 'react-router-dom';
import { Tab, Tabs,TabList, TabPanel } from "react-tabs";
import '../styles/Tabs.css';

function TabMainMenu() {
    const navigate = useNavigate();

    return (
        <>
            <Tabs className="flex h-[100px] justify-center">
            <TabList className="fixed mt-8 mainMenu-tabs__tab-list">
                <Tab selectedClassName="mainMenu-tabs__tab--selected" className='mainMenu-tabs__tab' onClick={ () => navigate('/items')}>管理商品</Tab>
                <Tab selectedClassName="mainMenu-tabs__tab--selected" className='mainMenu-tabs__tab' onClick={ () => navigate('/shoppinglist')}>お買い物リスト</Tab>
                <Tab selectedClassName="mainMenu-tabs__tab--selected" className='mainMenu-tabs__tab' onClick={ () => navigate('/setting')}>設定</Tab>
            </TabList>
            <TabPanel />
            <TabPanel />
            <TabPanel />
            </Tabs>
        </>

)};
export default TabMainMenu;