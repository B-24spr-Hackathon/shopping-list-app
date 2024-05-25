import React, { useEffect} from "react";
import { useNavigate } from "react-router-dom";

function LineLoginError() {
    const navigate = useNavigate();

    useEffect(() => {
        const timer = setTimeout(() => {
            navigate('/');
        }, 5000);

        return () => clearTimeout(timer);
    }, [navigate]);

    return (
        <>
        <div>LINEログインエラーです。</div>
        <div>5秒後自動的ににログインページに戻ります。</div>
        <div style={{cursor: "pointer", color: "blue", textDecoration: "underline"}}
                 onClick={() => navigate('/')}>
                戻らない場合はこちらをクリック
            </div>
        </>
    );
}

export default LineLoginError;