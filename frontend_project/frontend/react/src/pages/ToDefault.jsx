import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchUserInfoRequest } from '../utils/Requests';
import { useDispatch, useSelector } from 'react-redux';
import { setUser } from '../reducers/userSlice';
import { setSelectedList } from '../reducers/selectedListSlice';

const ToDefault = () => {
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const lists = useSelector(state => state.user.lists);
    const default_list = useSelector(state => state.user.default_list);
    const token = useSelector(state => state.token.token);

    useEffect(() => {
        const fetchUserInfo = async () => {
            const response = await fetchUserInfoRequest(token);
            dispatch(setUser(response.data.user));
            dispatch(setUser({lists:response.data.lists}));
            if(response.data.lists.length > 0){
                dispatch(setSelectedList(response.data.lists[response.data.lists.length -1]));
            }else{
                navigate('/home');
                return;
            }
            
            
            if (default_list) {
                navigate('/items');
            } else {
                navigate('/shoppinglist');
            }
        }
        fetchUserInfo();
    }, [navigate]);

    return null;
};

export default ToDefault;
