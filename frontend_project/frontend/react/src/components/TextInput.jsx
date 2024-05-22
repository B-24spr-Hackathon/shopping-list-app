import React from "react";

function TextInput({ type = "text", placeholder = "text", value, onChange }) {
    return (
        <div className="my-2 box-border flex justify-center">
            <input className="w-80 h-10 border-solid border-2 rounded-xl px-4"
                type={type}
                placeholder={placeholder}
                value={value}
                onChange={onChange} // 親コンポーネントから渡される onChange ハンドラを使用
            />
        </div>
    );
}

function TextInput2({ type = "text", placeholder = "text", value, onChange }) {
    return(
        <div class="min-w-full space-y-3 border">
            <input
                type={type}
                class="py-3 px-4 block w-full border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-neutral-400 dark:placeholder-neutral-500 dark:focus:ring-neutral-600" 
                placeholder={placeholder}
                value={value}
                onChange={onChange}
                />
        </div>
    )
}

export { TextInput, TextInput2 };