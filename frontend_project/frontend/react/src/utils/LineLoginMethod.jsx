import React, { useEffect, useState } from "react";
import { useCookies } from 'react-cookie';
import { useNavigate } from 'react-router-dom';
import { Header, Footer } from "../components/HeaderImg";
import { TextInput } from "../components/TextInput";
import { CertifyBtn, LineBtn } from "../components/Buttons";
import { Title, Bar, RegisterOrLogin } from "../components/Title";
import { useDispatch } from 'react-redux';
import { setUser,clearUser } from "../reducers/userSlice";
import { firstLineLoginRequest, lineLoginRequest, loginRequest } from "../utils/Requests";
import { useLocation } from "react-router-dom";
import { setToken } from "../reducers/tokenSlice";

function LineLoginMethod() {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const location = useLocation();
    const [cookies, setCookie] = useCookies(['jwt_token']);
    const [error, setError] = useState("");
    const [lineId, setLineId] = useState("");

    useEffect(() => {
        const queryParams = new URLSearchParams(location.search);
        const lineId = queryParams.get('line_id');
        if(lineId){
            handleLineLogin(lineId);
        }else{
            setError('LINE IDが見つかりません。')
        }
    })

    //ログイン関数

    const handleLineLogin = async(lineId) => {
        try{
            const response = await lineLoginRequest(lineId);
            console.log("LINE Login:", response);
            const token = response.data.access;
            // レスポンスからトークンを取得;
            setCookie('jwt_token', token, { path: '/', maxAge:100000, sameSite: "none", secure: true});
            //レスポンスでユーザー情報を受け取ってstoreに保存
            // dispatch(setUser(response.data.user));
            dispatch(setToken(token));
            //リダイレクト
            navigate('/todefault');
        }catch(err){
            console.log(err.response.data);

        };
    }



    return (
        <div>
            {error && <p>{error}</p>}
            {!error && <p>ログイン処理中...</p>}
        </div>
    );
}


export default LineLoginMethod;