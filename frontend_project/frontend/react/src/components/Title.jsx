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

export { Title, Bar };