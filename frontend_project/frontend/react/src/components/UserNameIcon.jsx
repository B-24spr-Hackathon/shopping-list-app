import React from "react";
import { useSelector } from 'react-redux';

function UserNameAndIcon() {
    const user_name = useSelector((state) => state.user.user_name);
    return (
        <>
            <img alt="img" />
            <div>{user_name}</div>

        </>

    );
}

export default UserNameAndIcon;