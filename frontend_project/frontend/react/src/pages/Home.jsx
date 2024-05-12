import React from "react";
import { useNavigate } from 'react-router-dom';
import { TestBtn } from "../components/Buttons";
import { useSelector } from 'react-redux';
import axios from "axios";
import { useCookies } from 'react-cookie';
import { apiRequest } from "../utils/Requests";
import { apiEndpoint } from "../utils/Requests";

function Home() {
    const navigate = useNavigate();
    const user_id = useSelector((state) => state.user.user_id);
    const user_name = useSelector((state) => state.user.user_name);
    const [cookies] = useCookies(['jwt_token']);

    //default_listを更新する処理
    const handleChangeDefault_list = async() => {
        const response = await apiRequest(
            'PATCH', apiEndpoint.user, {default_list: true}, "", true
        );
    }

    const handleFetchUserInfo = async() => {
        const response = await apiRequest(
            'GET', apiEndpoint.user, "", "", true
        );
        }

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
            <TestBtn onClick={handleChangeDefault_list} children="change" />
            <TestBtn onClick={handleFetchUserInfo} children="get" />

        </>

    );
}


export default Home;