import React from 'react';
import TabMainMenu from "../components/TabMainMenu";
import { Header, Footer } from "../components/HeaderImg";
import ListField from '../components/ListField';
import UserNameAndIcon from '../components/UserNameIcon';

function ShoppingList() {
    return (
        <>
            <Header />
            <UserNameAndIcon />


                <TabMainMenu />
                <div className='flex justify-center mt-4'>

                <ListField />
                </div>
            <Footer />
        </>

    );
}


export default ShoppingList;