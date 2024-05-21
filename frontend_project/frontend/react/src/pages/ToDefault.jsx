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
            try {
                const userInfo = await fetchUserInfoRequest(token);
                dispatch(setUser(userInfo.data));
                if (userInfo.data.lists.length === 0) {
                    navigate('/home');
                } else {
                    if (default_list) {
                        navigate('/items');
                    } else {
                        navigate('/shoppinglist');
                    }
                }
            } catch (err) {
                console.log(err);
            }
        };

        fetchUserInfo();
    }, [dispatch, navigate, token, default_list]);

    return null;
};

export default ToDefault;
