import React from "react";

function TextInput({ type = "text", placeholder = "text", value, onChange }) {
    return (
        <div className="my-3 box-border flex justify-center">
            <input className="w-80 h-12 border-solid border-2 rounded-xl px-4"
                type={type} 
                placeholder={placeholder} 
                value={value} 
                onChange={onChange} // 親コンポーネントから渡される onChange ハンドラを使用
            />
        </div>
    );
}

export default TextInput;