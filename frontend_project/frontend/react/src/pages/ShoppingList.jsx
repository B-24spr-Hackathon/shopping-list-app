import React from 'react';
import TabMainMenu from "../components/TabMainMenu";
import { Header, Footer } from "../components/HeaderImg";
import UserNameAndIcon from '../components/UserNameIcon';
import { ShoppingListPanel } from '../components/ListPanels';
import LogoutButton from '../components/Logout';
import { SelectList } from '../components/SelectBox';

function ShoppingList() {
    return (
        <>
            <Header />
            <LogoutButton />
            <UserNameAndIcon />


                <TabMainMenu />
                <SelectList />
                <div className='flex justify-center mt-4'>

                <ShoppingListPanel />
                </div>
            <Footer />
        </>

    );
}


export default ShoppingList;