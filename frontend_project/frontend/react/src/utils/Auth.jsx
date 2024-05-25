import React, { createContext, useContext, useState, useEffect } from 'react';
import { useCookies } from 'react-cookie';
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { resetAppState } from '../reducers/actionCreator';


const AuthContext = createContext(null);

export function useAuth() {
    return useContext(AuthContext);
}

export const AuthProvider = ({ children }) => {
    const [cookies] = useCookies(['jwt_token']);
    const [isLogin, setIsLogin] = useState(false);
    const navigate =useNavigate();
    const dispatch = useDispatch();

    useEffect(() => {
        const token = cookies.jwt_token;
        if(token) {
            setIsLogin(true);
        } else {
            setIsLogin(false);
            dispatch(resetAppState());
            if (window.location.pathname !== '/signup' &&
                window.location.pathname !== '/lineloginform' &&
                window.location.pathname !== '/lineloginerror' &&
                window.location.pathname !== '/lineloginmethod'){
                navigate('/');
            }
        }
    }, [cookies, navigate]);
    return (
        <AuthContext.Provider value={{ isLogin }}>
            { children }
        </AuthContext.Provider>
    );
};