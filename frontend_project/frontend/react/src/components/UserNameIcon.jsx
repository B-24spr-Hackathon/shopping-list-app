import React from "react";
import { useSelector } from 'react-redux';
import axios from "axios";

// export const FetchUserInfo = async() => {
//     try {
//         const response = await axios({
//             withCredentials: true,
//             method: "GET",
//             url: 'http://127.0.0.1:8000/api/user/',
            
            
//         });
//         console.log(response);
//         console.log(response.data);
//     } catch (err) {
//         console.log('Failure in fetch setup:', err);
//     }
// };
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