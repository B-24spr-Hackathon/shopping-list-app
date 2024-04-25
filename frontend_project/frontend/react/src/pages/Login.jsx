import React from "react";
import Header from "../components/Header";
import TextInput from "../components/TextInput";
import { CertifyBtn } from "../components/Buttons";

function Login() {
    return (
        <>
            <Header />
            <div className="">メールアドレスでログイン</div>
            <div className="">
                <TextInput  placeholder="mail"/>
                <TextInput  type="password" placeholder="password"/>
            </div>
            <div>
                <CertifyBtn onClick="#" children="ログインする"/>
            </div>
        </>

    );
}


export default Login;