import React from "react";

function CertifyBtn({ onClick, children }) {
    return <button className="bg-base-orange text-white px-24 py-2.5 rounded-full text-l my-2 font-medium" onClick={onClick}>{children}</button>;
}

function LineBtn({ onClick, children, disabled }) {
    return <button className="bg-line-green text-white px-8 py-2.5 rounded-full text-xl my-2 font-hel font-semibold disabled:opacity-50 disabled:pointer-events-none" onClick={onClick} disabled={disabled}>{children}</button>
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
    return <button className="py-2 px-2 w-full sm:w-24 md:w-24 lg:w-24 inline-flex items-center justify-center gap-x-2 text-sm font-semibold rounded-full border border-transparent bg-base-orange text-white hover:bg-base-orange-hover disabled:opacity-50 disabled:pointer-events-none disabled:opacity-50" onClick={onClick} disabled={disabled}>{children}</button>
}
function BoughtOrPassBtn({ onClick, children, disabled }) {
    return <button className="py-2 px-2 w-full sm:w-24 md:w-24 lg:w-24 inline-flex items-center justify-center gap-x-2 text-sm font-semibold rounded-full border border-transparent bg-base-orange text-white hover:bg-base-orange-hover disabled:opacity-50 disabled:pointer-events-none disabled:opacity-50" onClick={onClick} disabled={disabled}>{children}</button>
}
function DeleteListBtn({ onClick, children }) {
    return <button className="h-8 w-1/2 rounded-full text-white bg-base-orange border" onClick={onClick} >{children}</button>
}
function OrangeBtn({ onClick, children, disabled }){
    return <button type="button" onClick={onClick} disabled={disabled} class="py-3 px-4 w-60 justify-center inline-flex items-center gap-x-2 text-lg font-medium rounded-lg border border-gray-200 bg-base-orange text-white shadow-sm hover:bg-base-orange-hover disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:hover:bg-neutral-800">
            {children}
            </button>
}
export { CertifyBtn,OrangeBtn, LineBtn, TestBtn, ShoppingBtn, AddBtn, ToShoppingListBtn, BoughtOrPassBtn, DeleteListBtn }