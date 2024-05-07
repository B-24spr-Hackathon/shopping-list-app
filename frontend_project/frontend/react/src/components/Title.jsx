import React from "react";

function Title( {children} ) {
    return (
        <div className="flex justify-center font-bold text-2xl my-8">
            {children}
        </div>
    );
}

function Bar( {children} ){
    return (
        <div className="header-border my-3">
            {children}
        </div>
    );
}

function RegisterOrLogin( {children, onClick} ) {
    return (
        <div className="cursor-pointer text-base-orange flex justify-center text-sm my-3" onClick={onClick}>
            {children}
        </div>
    );
}
export { Title, Bar, RegisterOrLogin};