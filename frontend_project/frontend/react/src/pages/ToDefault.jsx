import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchUserInfoRequest } from '../utils/Requests';
import { useDispatch, useSelector } from 'react-redux';
import { setUser } from '../reducers/userSlice';

const ToDefault = () => {
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const default_list = useSelector(state => state.user.default_list);
    useEffect(() => {
        const fetchUserInfo = async () => {
            const response = await fetchUserInfoRequest();
            dispatch(setUser(response.data.user));
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
