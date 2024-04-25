import React from "react";

function TextInput({type="text", placeholder="text"}) {
    return (
        <div>
            <input type={type} placeholder={placeholder}/>
        </div>
    );
}

export default TextInput;