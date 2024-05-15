import React from 'react';
import { useCookies } from 'react-cookie';
import { useDispatch } from 'react-redux';
import { resetAppState } from '../reducers/actionCreator';
import { useNavigate } from 'react-router-dom';

function LogoutButton() {
    const [cookies, setCookie, removeCookie] = useCookies(['jwt_token']);
    const dispatch = useDispatch();
    const navigate = useNavigate();

    const handleLogout = () => {
        // クッキーからJWTトークンを削除
        removeCookie('jwt_token', { path: '/' });

        // アプリケーションのステートをリセット
        dispatch(resetAppState());

        // ログイン画面など、任意の画面にリダイレクト
        navigate('/');
    };

    return (
        <button onClick={handleLogout}>ログアウト</button>
    );
}

export default LogoutButton;