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
        <button onClick={handleLogout} type="button" className=''>
            <FontAwesomeIcon icon={faRightFromBracket} className="text-gray-500 text-4xl" />
            
        </button>
        </>

    );
}

export default LogoutButton;