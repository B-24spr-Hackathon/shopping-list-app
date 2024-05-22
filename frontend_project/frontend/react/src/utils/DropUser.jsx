import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { dropUserRequest, lineLinkRequest } from "./Requests"
import { TestBtn } from "../components/Buttons";
import { useNavigate } from "react-router-dom";
import { setLineLink } from "../reducers/lineLinkSlice";
import { useCookies } from 'react-cookie';
import { resetAppState } from '../reducers/actionCreator';


const DropUserBtn = () => {
    const token = useSelector(state => state.token.token);
    const navigate = useNavigate();
    const dispatch = useDispatch();

    const [cookies, setCookie, removeCookie] = useCookies(['jwt_token']);

    const handleDropUser = async() => {
        console.log(token);
        const confirmDrop = window.confirm('ユーザー情報を削除して退会します。本当によろしいですか？');
    
    if (confirmDrop) {
        const response = await dropUserRequest(token);
        removeCookie('jwt_token', { path: '/' });

        console.log('dropUser', response);
        dispatch(resetAppState());
    }
}
    return (
        <button onClick={handleDropUser} className="text-red-500">
            ユーザー情報を削除して退会する
        </button>

    )
}

export default DropUserBtn;