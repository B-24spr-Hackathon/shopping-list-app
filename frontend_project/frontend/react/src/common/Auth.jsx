import React, { createContext, useContext, useState, useEffect } from 'react';
import { useCookies } from 'react-cookie';
import { useNavigate } from 'react-router-dom';

const AuthContext = createContext(null);

export function useAuth() {
    return useContext(AuthContext);
}

export const AuthProvider = ({ children }) => {
    const [cookies] = useCookies(['jwt_token']);
    const [isLogin, setIsLogin] = useState(false);
    const navigate =useNavigate();

    useEffect(() => {
        const token = cookies.jwt_token;
        if(token) {
            setIsLogin(true);
        } else {
            setIsLogin(false);
            if(window.location.pathname !== '/signup'){
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