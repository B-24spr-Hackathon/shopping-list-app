import React, { useState } from "react";
import { useCookies } from 'react-cookie';
import { useNavigate } from 'react-router-dom';
import { Header, Footer } from "../components/HeaderImg";
import TextInput from "../components/TextInput";
import { CertifyBtn, LineBtn } from "../components/Buttons";
import { Title, Bar, RegisterOrLogin } from "../components/Title";
import { useDispatch } from 'react-redux';
import { setUser,clearUser } from "../reducers/userSlice";
import { loginRequest } from "../utils/Requests";
import { setToken } from "../reducers/tokenSlice";

function Login() {
    const dispatch = useDispatch();
    //状態管理
    const [cookies, setCookie] = useCookies(['jwt_token']);
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    //ログイン関数
    const navigate = useNavigate();

    const handleLogin = async() => {
        try{
            const response = await loginRequest(email, password);
            console.log("login:", response);
            const token = response.data.access;
            // レスポンスからトークンを取得;
            setCookie('jwt_token', token, { path: '/', maxAge:100000, sameSite: "none", secure: true});
            //レスポンスでユーザー情報を受け取ってstoreに保存
            dispatch(setUser(response.data.user));
            dispatch(setToken(token));
            //リダイレクト
            navigate('/todefault');
        }catch(err){
            console.log(err.response.data);
            setError("入力した情報で登録されていません。")

        };
    }



    return (
        <>
            <div className="flex flex-col">
                <Header />
                <div className="flex flex-col justify-center flex-grow items-center overflow-auto">
                    <Title children="ログイン" />
                    <LineBtn onClick={() => window.location.href='https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id=2004751038&redirect_uri=https%3A%2F%2F127.0.0.1%3A8000%2Fapi%2Fcallback%2F&state=shopping-list12345&bot_prompt=aggressive&scope=profile%20openid'} children="LINEでログイン"/>
                    <Bar children="またはメールアドレスでログイン"/>
                    <TextInput  type="email" placeholder="メールアドレス" value={email} onChange={e => setEmail(e.target.value)} />
                    <TextInput  type="password" placeholder="パスワード" value={password} onChange={e => setPassword(e.target.value)} />
                    <CertifyBtn onClick={handleLogin} children="ログインする"/>
                    <RegisterOrLogin children="新規登録はこちらから" onClick={ () => navigate('/signup')} />
                    {error && <p className="text-red-500">{error}</p>} { }
                </div>
                <Footer />
            </div>
        </>

    );
}


export default Login;