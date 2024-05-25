import React from 'react';

function Header() {
    return (
        <>
            <div className='fixed top-0 left-0 w-full h-[70px] bg-white opacity-100 z-100'>
                <img src="/HeaderBar.png" alt="img" className="block w-full h-full"/>
            </div>
        </>
    );
}

function Footer() {
    return (
        <div className='fixed  bottom-0 left-0 w-full h-[100px] bg-white opacity-100'>
            <img src="/HeaderBar.png" alt="img" className="block w-full h-full transform rotate-180"/>
        </div>
    );
}

export { Header, Footer };