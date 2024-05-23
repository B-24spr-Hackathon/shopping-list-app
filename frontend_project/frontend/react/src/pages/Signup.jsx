import React, { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import { Header, Footer } from "../components/HeaderImg";
import { TextInput } from "../components/TextInput";
import { CertifyBtn, LineBtn } from "../components/Buttons";
import { Title, Bar, RegisterOrLogin } from "../components/Title";
import { useDispatch } from 'react-redux';
import { setUser, clearUser } from "../reducers/userSlice";
import { useCookies } from 'react-cookie';
import { lineUrl, signUpRequest } from "../utils/Requests";
import { setToken } from "../reducers/tokenSlice";

function Signup({ toggleForm }) {
    const [user_id, setUser_id] = useState("");
    const [user_name, setUser_name] = useState("");
    const [email, setEmail] = useState("");
    const [password1, setPassword1] = useState("");
    const [password2, setPassword2] = useState("");
    const [error, setError] = useState("");
    const [emailError, setEmailError] = useState('');
    const [passwordError, setPasswordError] = useState('');
    const dispatch = useDispatch();
    const [cookies, setCookie] = useCookies(['jwt_token']);
    const navigate = useNavigate();

    useEffect(() => {
        validateEmail(email);
    }, [email]);

    useEffect(() => {
        if (password1 && password2 && password1 !== password2) {
            setPasswordError("パスワードが一致しません");
        } else {
            setPasswordError("");
        }
    }, [password1, password2]);

    const validateEmail = (email) => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email) && email) {
            setEmailError('無効なメールアドレス形式です。');
        } else {
            setEmailError('');
        }
    };

    const handleSignup = async () => {
        if (passwordError || emailError) return;
        if (!user_id || !user_name || !email || !password1 || !password2) return;
        try {
            const response = await signUpRequest(user_id, user_name, email, password1);
            const token = response.data.access;
            setCookie('jwt_token', token, { path: '/', maxAge: 100000, sameSite: "none", secure: true });
            // dispatch(setUser(response.data.user));
            dispatch(setToken(token));
            navigate('/todefault');
        } catch (err) {
            setError("他のユーザーが使用中のユーザーIDです");
            console.error('error;', err);
        }
    };

    return (
        <div className="flex flex-col items-center">
            <Header />
            <div className="flex flex-col justify-center items-center overflow-auto mb-1">
                <Title children="IDを登録" />
                <LineBtn onClick={() => window.location.href = lineUrl} children="LINEでログイン" />
                <Bar children="またはメールアドレスで登録" />
                <TextInput placeholder="ユーザーID" value={user_id} onChange={e => setUser_id(e.target.value)} />
                <TextInput placeholder="名前" value={user_name} onChange={e => setUser_name(e.target.value)} />
                <TextInput type="email" placeholder="メールアドレス" value={email} onChange={e => setEmail(e.target.value)} />
                <TextInput type="password" placeholder="パスワード" value={password1} onChange={e => setPassword1(e.target.value)} />
                <TextInput type="password" placeholder="パスワード(確認)" value={password2} onChange={e => setPassword2(e.target.value)} />
                <CertifyBtn onClick={handleSignup} children="登録する" />
                <RegisterOrLogin children="すでにお持ちのアカウントでログインする" onClick={toggleForm} />
                {emailError && <p className="text-red-500">{emailError}</p>}
                {passwordError && <p className="text-red-500">{passwordError}</p>}
                {error && <p className="text-red-500">{error}</p>}
            </div>
        </div>
    );
}

export default Signup;
