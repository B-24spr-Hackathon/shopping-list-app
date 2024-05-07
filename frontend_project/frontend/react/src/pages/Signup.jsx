import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';
import axios from "axios";
import { Header, Footer } from "../components/HeaderImg";
import TextInput from "../components/TextInput";
import { CertifyBtn, LineBtn } from "../components/Buttons";
import { Title, Bar, RegisterOrLogin } from "../components/Title";

function Signup() {
    //状態管理
    const [user_id, setUser_id] = useState("");
    const [user_name, setUser_name] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    //ユーザー登録関数
    const navigate = useNavigate();

    const handleSignup = async() => {
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/user/', {
                user_id:user_id,
                user_name: user_name,
                email: email,
                password: password,
            });
            console.log(response.data);
            //リダイレクト
            navigate('/home');

        } catch (err) {
            setError("失敗");
            console.error(err);
        }
    };
    return (
        <>
            <div className="flex flex-col min-h-screen">
                <Header />
                <div className="flex flex-col justify-center items-center flex-grow overflow-auto mb-1">
                    <Title children="IDを登録" />
                    <LineBtn onClick={""} children="LINEでログイン"/>
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