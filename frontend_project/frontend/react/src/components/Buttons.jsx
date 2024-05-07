import React from "react";

function CertifyBtn({ onClick, children }) {
    return <button className="bg-base-orange text-white px-24 py-2.5 rounded-full text-l my-2 font-medium" onClick={onClick}>{children}</button>;
}

function LineBtn({ onClick, children }) {
    return <button className="bg-line-green text-white px-8 py-2.5 rounded-full text-xl my-2 font-hel font-semibold" onClick={onClick}>{children}</button>
}


export { CertifyBtn, LineBtn }