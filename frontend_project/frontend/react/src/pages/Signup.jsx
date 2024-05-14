import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';
import axios from "axios";
import { Header, Footer } from "../components/HeaderImg";
import TextInput from "../components/TextInput";
import { CertifyBtn, LineBtn } from "../components/Buttons";
import { Title, Bar, RegisterOrLogin } from "../components/Title";
import { useDispatch } from 'react-redux';
import { setUser, clearUser } from "../reducers/userSlice";
import { useCookies } from 'react-cookie';
import { signUpRequest } from "../utils/Requests";

function Signup() {
    //状態管理
    const [user_id, setUser_id] = useState("");
    const [user_name, setUser_name] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const dispatch = useDispatch();
    const [cookies, setCookie] = useCookies(['jwt_token']);

    //ユーザー登録関数
    const navigate = useNavigate();

    const handleSignup = async() => {
        try {
            const response = await signUpRequest(user_id, user_name, email, password);
            console.log(response.data);
             // JWTトークンをクッキーに保存する
            const token = response.data.access; // レスポンスからトークンを取得;
            setCookie('jwt_token', token, { path: '/', maxAge:100000, sameSite: "none", secure: true});
            //レスポンスでユーザー情報を受け取ってstoreに保存
            dispatch(setUser( response.data.user ));
            //リダイレクト
            navigate('/home');

        } catch (err) {
            setError("失敗");
            console.error(err);
        }
    };
    return (
        <>
            <div className="flex flex-col items-center">
                <Header />
                <div className="flex flex-col justify-center items-center overflow-auto mb-1">
                    <Title children="IDを登録" />
                    <LineBtn onClick={() => window.location.href='https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id=2004751038&redirect_uri=https%3A%2F%2F127.0.0.1%3A8000%2Fapi%2Fcallback%2F&state=shopping-list12345&bot_prompt=aggressive&scope=profile%20openid'} children="LINEでログイン"/>
                    <Bar children="またはメールアドレスで登録"/>
                    <TextInput  placeholder="ユーザーID" value={user_id} onChange={e => setUser_id(e.target.value)} />
                    <TextInput  placeholder="名前" value={user_name} onChange={e => setUser_name(e.target.value)} />
                    <TextInput  type="email" placeholder="メールアドレス" value={email} onChange={e => setEmail(e.target.value)} />
                    <TextInput  type="password" placeholder="パスワード" value={password} onChange={e => setPassword(e.target.value)} />
                    <TextInput  type="password" placeholder="パスワード(確認)：未実装" />
                    <CertifyBtn onClick={handleSignup} children="登録する"/>
                    <RegisterOrLogin children="すでにお持ちのアカウントでログインする" onClick={ () => navigate('/')} />
                    {error && <p>{error}</p>} { }
                </div>
                <Footer />
            </div>
        </>

        

    );
}


export default Signup;