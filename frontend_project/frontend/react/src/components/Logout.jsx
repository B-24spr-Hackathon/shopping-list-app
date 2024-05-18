import React from 'react';
import { useCookies } from 'react-cookie';
import { useDispatch } from 'react-redux';
import { resetAppState } from '../reducers/actionCreator';
import { useNavigate } from 'react-router-dom';

function LogoutButton(  ) {
    const [cookies, setCookie, removeCookie] = useCookies(['jwt_token']);
    const dispatch = useDispatch();
    const navigate = useNavigate();

    const handleLogout = () => {
        // クッキーからJWTトークンを削除
        removeCookie('jwt_token', { path: '/' });

        // アプリケーションのステートをリセット
        dispatch(resetAppState());

        // ログイン画面など、任意の画面にリダイレクト
        //navigate('/');
    };

    return (
        <button onClick={handleLogout} type="button" class=" text-center py-3 px-4 inline-flex items-center gap-x-2 text-sm font-medium rounded-lg border border-gray-200 bg-white text-gray-500 shadow-sm hover:bg-gray-50 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-neutral-400 dark:hover:bg-neutral-800">
            ログアウト
        </button>

    );
}

export default LogoutButton;