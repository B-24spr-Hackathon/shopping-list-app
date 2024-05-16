import React from "react";
import { useSelector } from 'react-redux';


function UserNameAndIcon() {
    const user_name = useSelector((state) => state.user.user_name);
    return (
        <>
            <div className="mx-8 w-full h-[20px]">
                <img className="fixed" alt={user_name[0]} />
                <div className="fixed ml-8">{user_name}</div>
            </div>

        </>

    );
}

export default UserNameAndIcon;