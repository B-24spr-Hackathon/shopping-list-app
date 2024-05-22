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
            const memberStatusInfo = await fetchMemberStatusInfoRequest(token);
            dispatch(setMember(memberStatusInfo.data));
            // setMemberInfo(memberStatusInfo.data);
            console.log(selectedList)

            //リストが一つもないときhomeへ
            if(userInfoResponse.data.lists.length == 0){
                navigate("/home");
            //それ以外
            }else{
                //selectedListがあれば
                if(selectedList.list_id == null){
                    dispatch(setSelectedList(userInfo.lists[0]))
                }
                //デフォルトリストの値でitemsに遷移した後の表示を変える
                if (userInfo.default_list){
                    navigate('/items');
                }else{
                    navigate('/items');
                }
            }
        }

        fetchUserInfo();
    }, []);

    return null;
};

export default ToDefault;
