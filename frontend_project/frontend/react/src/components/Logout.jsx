import React from 'react';
import { useCookies } from 'react-cookie';
import { useDispatch } from 'react-redux';
import { resetAppState } from '../reducers/actionCreator';
import { useNavigate } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faRightFromBracket } from '@fortawesome/free-solid-svg-icons';

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
        navigate('/');
    };

    return (
        <>
        <button onClick={handleLogout} type="button" className='flex items-center gap-x-3.5 py-2  rounded-lg text-m text-gray-800  focus:outline-none focus:bg-gray-100 dark:text-neutral-400 dark:hover:bg-neutral-700 dark:hover:text-neutral-300 dark:focus:bg-neutral-700"'>
            ログアウト
        </button>
        </>

    );
}

export default LogoutButton;