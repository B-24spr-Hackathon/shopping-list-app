import React, { useState } from "react";
import axios from "axios";
import Header from "../components/Header";
import TextInput from "../components/TextInput";
import { CertifyBtn, LineBtn } from "../components/Buttons";
import Title from "../components/Title";
import Footer from "../components/Footer";

function Signup() {
    //状態管理
    const [user_id, setUser_id] = useState("");
    const [user_name, setUser_name] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    //ユーザー登録関数
    const handleSignup = async() => {
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/user/', {
                user_id:user_id,
                user_name: user_name,
                email: email,
                password: password,
            });
            console.log(response.data);

        } catch (err) {
            setError("失敗");
            console.error(err);
        }
    };
    return (
        <>
            <div className="main flex justify-center items-center flex-col">
                <Header />
                <Title children="IDを登録" />
                <LineBtn onClick={""} children="LINEで新規登録"/>
                <TextInput  placeholder="user_id" value={user_id} onChange={e => setUser_id(e.target.value)} />
                <TextInput  placeholder="user_name" value={user_name} onChange={e => setUser_name(e.target.value)} />
                <TextInput  placeholder="mail" value={email} onChange={e => setEmail(e.target.value)} />
                <TextInput  type="password" placeholder="password" value={password} onChange={e => setPassword(e.target.value)} />
                <CertifyBtn onClick={handleSignup} children="登録する"/>
                {error && <p>{error}</p>} { }
                <Footer />
            </div>
        </>

        

    );
}


export default Signup;