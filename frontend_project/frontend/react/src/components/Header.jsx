import React from 'react';
import "../styles/Header.css"

function Header() {
    return (
        <header className='header'>
            <img src="/HeaderBar.png" alt="img" className="w-full h-auto lg:h-[125px]"/>
        </header>
    );
}

export default Header;