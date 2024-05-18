import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { lineLinkRequest } from "./Requests"
import { LineBtn } from "../components/Buttons";
import { useNavigate } from "react-router-dom";
import { setLineLink } from "../reducers/lineLinkSlice";

const LineLinkBtn = () => {
    const token = useSelector(state => state.token.token);
    const userInfo = useSelector(state => state.user)
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const handleLineLink = async() => {
        console.log(token);
        const response = await lineLinkRequest(token);
        console.log('lineLink',response);
        console.log("line_status",userInfo.line_status);
        dispatch(setLineLink(response.data));
        navigate('/linelinkform');

    }
    return (
        <LineBtn
            onClick={handleLineLink}
            disabled={userInfo.line_status}
            children="LINEと連携する"
            />
    )
}

export default LineLinkBtn;