import React, { useState } from "react";
import Login from "./Login";
import Signup from "./Signup";
import { Bar } from "../components/Title";

function LoginNew() {
    const [isLogin, setIsLogin] = useState(true);

    const toggleForm = () => {
        setIsLogin(!isLogin);
    };

    return (

        <>
            <div className="flex flex-col items-center">
                <div className="flex justify-center my-4">
                    <img className="w-52 h-40 object-cover rounded-full" src="/kaimotto.jpeg"/>
                </div>
                <div className="text-center text-lg mt-1 mb-8 font-sans">
                   <Bar children='もっと上手にまとめ買い！無駄なく、もれなく、買いもっと！' />
                </div>
                    {isLogin ? (
                        <Login toggleForm={toggleForm} />
                    ) : (
                        <Signup toggleForm={toggleForm} />
                    )}
            </div>
        </>
    );
}

export default LoginNew;
