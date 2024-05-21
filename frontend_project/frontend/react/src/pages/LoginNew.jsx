import React, { useState } from "react";
import Login from "./Login";
import Signup from "./Signup";

function LoginNew() {
    const [isLogin, setIsLogin] = useState(true);

    const toggleForm = () => {
        setIsLogin(!isLogin);
    };

    return (
        <div className="flex flex-col items-center">
            {isLogin ? (
                <Login toggleForm={toggleForm} />
            ) : (
                <Signup toggleForm={toggleForm} />
            )}
        </div>
    );
}

export default LoginNew;
