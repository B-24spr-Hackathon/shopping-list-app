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

function LineLoginForm() {
    const dispatch = useDispatch();
    //状態管理
    const [cookies, setCookie] = useCookies(['jwt_token']);
    const [user_id, setUser_id] = useState("");
    const [user_name, setUser_name] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    //ログイン関数
    const navigate = useNavigate();

    const handleLogin = async() => {
        try{
            const data = await loginRequest(email, password);
            console.log("login:", data);
            const token = data.data.access;
            // レスポンスからトークンを取得;
            setCookie('jwt_token', token, { path: '/', maxAge:100000, sameSite: "none", secure: true});
            //レスポンスでユーザー情報を受け取ってstoreに保存
            dispatch(setUser(data.data.user));
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
                    <Title children="LINEログイン（機能未実装）" />
                    <Bar children="またはメールアドレスでログイン"/>
                    <TextInput  type="email" placeholder="メールアドレス未実装" value={email} onChange={e => setEmail(e.target.value)} />
                    <TextInput  type="password" placeholder="パスワード未実装" value={password} onChange={e => setPassword(e.target.value)} />
                    <CertifyBtn onClick={"handleLogin"} children="ログインする"/>
                    <RegisterOrLogin children="新規登録はこちらから" onClick={ () => navigate('/signup')} />
                    {error && <p>{error}</p>} { }
                </div>
                <Footer />
            </div>
        </>

    );
}


export default LineLoginForm;