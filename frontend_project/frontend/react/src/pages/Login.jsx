import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';
import axios from "axios";
import { Header, Footer } from "../components/HeaderImg";
import TextInput from "../components/TextInput";
import { CertifyBtn, LineBtn } from "../components/Buttons";
import { Title, Bar, RegisterOrLogin } from "../components/Title";

function Login() {
    //状態管理
    const [user_id, setUser_id] = useState("");
    const [user_name, setUser_name] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    //ログイン関数
    const navigate = useNavigate();

    const handleLogin = async() => {
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/login/', {
                email: email,
                password: password,
            });
            console.log(response.data);

             // JWTトークンをクッキーに保存する
            const token = response.data.access; // レスポンスからトークンを取得
            document.cookie = `jwt_token=${token}; path=/; max-age=3600`; // クッキーに保存。max-ageは有効期限(秒)
            
            //リダイレクト
            navigate('/home');

        } catch (err) {
            setError("失敗");
            console.error(err);
        }
    };
    return (
        <>
            <div className="flex flex-col">
                <Header />
                <div className="flex flex-col justify-center flex-grow items-center overflow-auto">
                    <Title children="ログイン" />
                    <LineBtn onClick={"#"} children="LINEでログイン"/>
                    <Bar children="またはメールアドレスでログイン"/>
                    <TextInput  type="email" placeholder="メールアドレス" value={email} onChange={e => setEmail(e.target.value)} />
                    <TextInput  type="password" placeholder="パスワード" value={password} onChange={e => setPassword(e.target.value)} />
                    <CertifyBtn onClick={handleLogin} children="ログインする"/>
                    <RegisterOrLogin children="新規登録はこちらから" onClick={ () => navigate('/signup')} />
                    {error && <p>{error}</p>} { }
                </div>
                <Footer />
            </div>
        </>

    );
}


export default Login;