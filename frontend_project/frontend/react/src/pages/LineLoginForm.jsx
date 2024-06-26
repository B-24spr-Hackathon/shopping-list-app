import React, { useEffect, useState } from "react";
import { useCookies } from 'react-cookie';
import { useNavigate } from 'react-router-dom';
import { Header, Footer } from "../components/HeaderImg";
import { TextInput } from "../components/TextInput";
import { CertifyBtn, LineBtn } from "../components/Buttons";
import { Title, Bar, RegisterOrLogin } from "../components/Title";
import { useDispatch } from 'react-redux';
import { setUser,clearUser } from "../reducers/userSlice";
import { firstLineLoginRequest, loginRequest } from "../utils/Requests";
import { useLocation } from "react-router-dom";
import { setToken } from "../reducers/tokenSlice";

function LineLoginForm() {
    const dispatch = useDispatch();
    //状態管理
    const [cookies, setCookie] = useCookies(['jwt_token']);
    const [error, setError] = useState("");
    const [userId, setUserId] = useState("");
    const [userName, setUserName] = useState("");
    const [lineId, setLineId] = useState("");
    const [lineStatus, setLineStatus] = useState("");
    const location = useLocation();

    useEffect(() => {
        const queryParams = new URLSearchParams(location.search);
        const lineId = queryParams.get('line_id');
        const userName = queryParams.get('user_name');
        const lineStatus = queryParams.get('status');
        if(lineId && userName && lineStatus){
            setLineId(lineId);
            setUserName(userName);
            setLineStatus(lineStatus);
        }
    })

    //ログイン関数
    const navigate = useNavigate();

    const handleLineLogin = async() => {
        try{
            const response = await firstLineLoginRequest(userId, userName, lineId, lineStatus);
            console.log("LINE Login:", response);
            const token = response.data.access;
            // レスポンスからトークンを取得;
            setCookie('jwt_token', token, { path: '/', maxAge:100000, sameSite: "none", secure: true});
            //レスポンスでユーザー情報を受け取ってstoreに保存
            dispatch(setUser(response.data.user));
            dispatch(setToken(token));
            //リダイレクト
            navigate('/home');
        }catch(err){
            console.log(err.response.data);

        };
    }



    return (
        <>
            <div className="flex flex-col">
                <Header />
                <div className="flex flex-col justify-center flex-grow items-center overflow-auto">
                <div className="flex justify-center my-4">
                    <img className="w-52 h-40 object-cover rounded-full" src="/kaimotto.jpeg"/>
                </div>
                    <Title children="LINEログイン" />
                    <Bar children="登録するユーザーIDを入力してください"/>
                    <TextInput  type="text" placeholder="user_id" value={userId} onChange={e => setUserId(e.target.value)} />
                    {/* <TextInput  type="text" placeholder="user_name未実装" value={password} onChange={e => setPassword(e.target.value)} /> */}
                    <LineBtn children="ログインする" onClick={handleLineLogin} disabled={!userId} />
                    <RegisterOrLogin children="メールアドレスでログインに戻る" onClick={ () => navigate('/')} />
                    {error && <p>{error}</p>} { }
                </div>
                <Footer />
            </div>
        </>

    );
}


export default LineLoginForm;