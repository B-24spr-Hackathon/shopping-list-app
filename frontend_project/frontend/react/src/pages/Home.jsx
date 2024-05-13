import React from "react";
import { useNavigate } from 'react-router-dom';
import { TestBtn } from "../components/Buttons";
import { useSelector } from 'react-redux';
import axios from "axios";
import { useCookies } from 'react-cookie';
import { fetchUserInfoRequest, apiRequest } from "../utils/Requests";
import { apiEndpoint } from "../utils/Requests";
import { useDispatch } from "react-redux";
import { setUser, clearUser } from "../reducers/userSlice";

function Home() {
    const dispatch = useDispatch();

    const navigate = useNavigate();
    const user_id = useSelector((state) => state.user.user_id);
    const user_name = useSelector((state) => state.user.user_name);

    const [cookies] = useCookies(['jwt_token']);


    const handleFetchUserInfo = async() => {
        try {
            const response = await fetchUserInfoRequest();
            console.log("fetch:",response.data);
            dispatch(setUser(response.data.user));
            dispatch(setUser({lists:response.data.lists}));
        }catch(err){
            // console.log(err.response.data);
            console.log("era-")
            console.log(err.response);
        };
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
            <TestBtn onClick={handleFetchUserInfo} children="get" />

        </>

    );
}


export default Home;