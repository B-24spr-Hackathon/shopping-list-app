import React from "react";

function TextInput({ type = "text", placeholder = "text", value, onChange }) {
    return (
        <div className="mt-8">
            <input 
                type={type} 
                placeholder={placeholder} 
                value={value} 
                onChange={onChange} // 親コンポーネントから渡される onChange ハンドラを使用
            />
        </div>
    );
}

export default TextInput;