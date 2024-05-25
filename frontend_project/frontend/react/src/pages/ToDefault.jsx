import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchItemsOfListRequest, fetchMemberStatusInfoRequest, fetchUserInfoRequest } from '../utils/Requests';
import { useDispatch, useSelector } from 'react-redux';
import { setUser } from '../reducers/userSlice';
import { setSelectedList } from '../reducers/selectedListSlice';
import { setMember } from '../reducers/memberSlice';

const ToDefault = () => {
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const lists = useSelector(state => state.user.lists);
    const token = useSelector(state => state.token.token);
    const userInfo = useSelector(state => state.user);
    const selectedList = useSelector(state => state.selectedList);

    useEffect(() => {
        const fetchUserInfo = async () => {
            //ユーザー情報とリスト情報を取得
            const userInfoResponse = await fetchUserInfoRequest(token);
            dispatch(setUser(userInfoResponse.data.user));
            dispatch(setUser({lists: userInfoResponse.data.lists}));

            //招待・申請情報を取得して保存
            const memberStatusInfoResponse = await fetchMemberStatusInfoRequest(token);
            dispatch(setMember(memberStatusInfoResponse.data));
            // setMemberInfo(memberStatusInfo.data);

            //リストがあれば、/shoppinglistへ
            if(userInfoResponse.data.lists.length != 0){
                //selectedListがなければ、リストの最初を設定する
                if(selectedList.list_id == null){
                    dispatch(setSelectedList(userInfoResponse.data.lists[0]))
                }
                navigate('/shoppinglist');
            //リストがなければ/homeへ
            }else{
                navigate("/home");
            }
        }

        fetchUserInfo();
    }, []);

    return (
        'データ読み込み中...'
    );
};

export default ToDefault;
