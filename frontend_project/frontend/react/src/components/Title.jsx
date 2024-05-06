import React from "react";

function Title( {children} ) {
    return (
        <div className="flex justify-center font-bold text-2xl mt-8">
            {children}
        </div>
    );
}

export default Title;