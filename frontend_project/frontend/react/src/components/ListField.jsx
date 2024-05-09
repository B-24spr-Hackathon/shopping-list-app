import React from 'react';
import '../styles/Lists.css'
import { ShoppingBtn } from './Buttons';

function ShoppingItems() {
    return(
        <>

              <div className='flex justify-center text-center items-center border-b'>
                    <img className='flex-none ' alt='ctg' />
                    <div className='flex-none' >商品名</div>
                    <div className='flex-none'>
                        <ShoppingBtn children="買った"/>
                    </div>
                    <div className='flex-none'>
                        <ShoppingBtn children="見送り"/>
                    </div>
              </div>



        </>
    )
}

function ListField() {
    return (
        <>
        <div className='list-field-container'>
            <div class="list-field-title">
                MyHome
            </div>
            <div class="list-field">
                <p className='text-center'>ここに日付</p>
                <ShoppingItems />
            </div>
        </div>
        </>
    )
}

export default ListField;