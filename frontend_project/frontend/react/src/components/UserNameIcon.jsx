import React from "react";
import { useSelector } from 'react-redux';

function UserNameAndIcon() {
    const user_name = useSelector((state) => state.user.user_name);
    const initial = user_name ? user_name[0].toUpperCase() : '';

    return (
        <div className="flex items-center mx-8 w-full h-[20px]">
            <div className="fixed bg-green-700 text-white rounded-full w-8 h-8 flex items-center justify-center">
                {initial}
            </div>
            <div className="fixed mx-10 text-xl">{user_name}</div>
        </div>
    );
}
function OtherUserNameAndIcon({userInfo}) {
    if (!userInfo) {
        return null; // userInfoがない場合は何も表示しない
    }

    const initial = userInfo[0].toUpperCase();

    return (
        <div className="flex items-center">
            <div className="bg-pink-500 text-white rounded-full w-8 h-8 flex items-center justify-center">
                {initial}
            </div>
            <div className="mx-3 text-xl">{userInfo}</div>
        </div>
    );
}

export {UserNameAndIcon, OtherUserNameAndIcon};
