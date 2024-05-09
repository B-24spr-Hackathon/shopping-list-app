import React from "react";
import { useNavigate } from 'react-router-dom';
import { TestBtn } from "../components/Buttons";
import { useSelector } from 'react-redux';

function Home() {
    const navigate = useNavigate();
    const user_id = useSelector((state) => state.user.user_id);
    const user_name = useSelector((state) => state.user.user_name);

    return (
        <>
            <TestBtn onClick={ () => navigate('/items')} children="itemsへ"/>
            <div></div>
            <TestBtn onClick={ () => navigate('/list')} children="listへ"/>
            <div>
                {user_name ? (
                    <p>ようこそ、{user_name}さん（ユーザーID: {user_id}）！</p>
                ) : (
                    <p>ログイン情報がありません。</p>
                )}
            </div>

        </>

    );
}


export default Home;