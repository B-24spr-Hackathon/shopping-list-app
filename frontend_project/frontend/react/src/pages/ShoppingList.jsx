import React from 'react';
import TabMainMenu from "../components/TabMainMenu";
import { Header, Footer } from "../components/HeaderImg";
import UserNameAndIcon from '../components/UserNameIcon';
import { ShoppingListPanel } from '../components/ListPanels';

function ShoppingList() {
    return (
        <>
            <Header />
            <UserNameAndIcon />


                <TabMainMenu />
                <div className='flex justify-center mt-4'>

                <ShoppingListPanel />
                </div>
            <Footer />
        </>

    );
}


export default ShoppingList;