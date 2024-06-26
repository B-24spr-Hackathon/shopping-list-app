import React, { useEffect, useState } from "react";
import { useCookies } from 'react-cookie';
import { useNavigate } from 'react-router-dom';
import { Header, Footer } from "../components/HeaderImg";
import { TextInput } from "../components/TextInput";
import { CertifyBtn, LineBtn } from "../components/Buttons";
import { Title, Bar, RegisterOrLogin } from "../components/Title";
import { useDispatch, useSelector } from 'react-redux';
import { setUser, clearUser } from "../reducers/userSlice";
import { fetchUserInfoRequest, lineUrl, loginRequest } from "../utils/Requests";
import { setToken } from "../reducers/tokenSlice";



function Login({ toggleForm }) {
    const dispatch = useDispatch();
    const [cookies, setCookie] = useCookies(['jwt_token']);
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState([]);
    const navigate = useNavigate();
    const token = useSelector(state => state.token.token);

    useEffect(()=> {
        const haveJwt = async()=>{
            try{
                const response = await fetchUserInfoRequest(token);
                navigate('/todefault');
            }catch(err){
                console.error(err);
            }
        }
        haveJwt();
    }, []);

    const handleLogin = async () => {
        try {
            const response = await loginRequest(email, password);
            console.log("login:", response);
            //tokenをstateとブラウザに保存
            const token = response.data.access;
            setCookie('jwt_token', token, { path: '/', maxAge: 100000, sameSite: "none", secure: true });
            dispatch(setToken(token));
            navigate('/todefault');

        } catch (err) {
            if (err.response) {
                const errData = err.response.data;
                const errs = [];
                for (const key in errData) {
                  if (errData.hasOwnProperty(key)) {
                    errs.push(`${errData[key]}`);
                  }
                }
                setError(errs);
              } else {
                setError(['Network error']);
              }
        };
    };

    return (
        <div className="flex flex-col">
            <Header />
            <div className="flex flex-col justify-center flex-grow items-center overflow-auto">
                <Title children="ログイン" />
                <LineBtn onClick={() => window.location.href = lineUrl} children="LINEでログイン" />
                <Bar children="またはメールアドレスでログイン" />
                <TextInput type="email" placeholder="メールアドレス" value={email} onChange={e => setEmail(e.target.value)} />
                <TextInput type="password" placeholder="パスワード" value={password} onChange={e => setPassword(e.target.value)} />
                <CertifyBtn onClick={handleLogin} children="ログインする" disabled={!email || !password} />
                <RegisterOrLogin children="新規登録はこちらから" onClick={toggleForm} />
                {error && <p className="text-red-500">{error}</p>}
            </div>
        </div>
    );
}

export default Login;
