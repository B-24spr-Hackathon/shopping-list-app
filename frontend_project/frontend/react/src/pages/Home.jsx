import React from "react";
import { useNavigate } from 'react-router-dom';
import { testBtn } from "../components/Buttons";

function Home() {
    const navigate = useNavigate();
    return (
        <>
            <testBtn onClick={ () => navigate('/items')} children="itemsへ"/>
            <div></div>
            <testBtn onClick={ () => navigate('/list')} children="listへ"/>
        </>

    );
}


export default Home;