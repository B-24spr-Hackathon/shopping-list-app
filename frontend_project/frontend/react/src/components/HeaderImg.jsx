import React from 'react';

function Header() {
    return (
        <>
            <div className='top-0 left-0 w-full h-[120px]'>
                <img src="/HeaderBar.png" alt="img" className="block w-full h-full"/>
            </div>
        </>
    );
}

function Footer() {
    return (
        <div className='bottom-0 left-0 w-full h-[120px]'>
            <img src="/HeaderBar.png" alt="img" className="block w-full h-full transform rotate-180"/>
        </div>
    );
}

export { Header, Footer };