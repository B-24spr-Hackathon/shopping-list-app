import React from "react";

function CertifyBtn({ onClick, children }) {
    return <button className="bg-base-orange text-white px-24 py-2.5 rounded-full text-l my-2 font-medium" onClick={onClick}>{children}</button>;
}

function LineBtn({ onClick, children }) {
    return <button className="bg-line-green text-white px-8 py-2.5 rounded-full text-xl my-2 font-hel font-semibold" onClick={onClick}>{children}</button>
}

function TestBtn({ onClick, children }) {
    return <button className="py-3 px-4 inline-flex items-center gap-x-2 text-sm font-semibold rounded-full border border-transparent bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 disabled:pointer-events-none" onClick={onClick}>{children}</button>
}

function ShoppingBtn({ onClick, children }) {
    return <button className="bg-base-orange text-white px-8 py-2 rounded-full text-l my-2 font-medium " onClick={onClick}>{children}</button>;
}

function AddBtn({ onClick, children }) {
    return <button className="h-12 w-12 rounded-full bg-white border" onClick={onClick}>{children}</button>
}
function ToShoppingListBtn({ onClick, children, disabled }) {
    return <button className="py-3 px-4 inline-flex items-center gap-x-2 text-sm font-semibold rounded-full border border-transparent bg-base-orange text-white hover:bg-base-orange-hover disabled:opacity-50 disabled:pointer-events-none disabled:opacity-50" onClick={onClick} disabled={disabled}>{children}</button>
}
function BoughtOrPassBtn({ onClick, children, disabled }) {
    return <button className="h-8 w-1/2 rounded-full text-white bg-base-orange border" onClick={onClick} disabled={disabled}>{children}</button>
}
function DeleteListBtn({ onClick, children }) {
    return <button className="h-8 w-1/2 rounded-full text-white bg-base-orange border" onClick={onClick} >{children}</button>
}

export { CertifyBtn, LineBtn, TestBtn, ShoppingBtn, AddBtn, ToShoppingListBtn, BoughtOrPassBtn, DeleteListBtn }