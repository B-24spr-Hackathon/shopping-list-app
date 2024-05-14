import React, { useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import { AddBtn, TestBtn } from "../components/Buttons";
import { useSelector } from 'react-redux';
import axios from "axios";
import { useCookies } from 'react-cookie';
import { fetchUserInfoRequest, apiRequest } from "../utils/Requests";
import { apiEndpoint } from "../utils/Requests";
import { useDispatch } from "react-redux";
import { setUser, clearUser } from "../reducers/userSlice";
import { Footer, Header } from "../components/HeaderImg";
import { Title } from "../components/Title";
import { SelectList } from "../components/SelectBox";
import AddNewList from "../utils/AddNewList";
import { setSelectedList } from "../reducers/selectedListSlice";

function Home() {
    const dispatch = useDispatch();

    const navigate = useNavigate();
    const user_id = useSelector((state) => state.user.user_id);
    const user_name = useSelector((state) => state.user.user_name);
    const lists = useSelector(state => state.user.lists);
    const handleAddNewList = AddNewList();
    const [cookies] = useCookies(['jwt_token']);

    

    const handleFetchUserInfo = async() => {
        try {
            const response = await fetchUserInfoRequest();
            console.log("fetch:",response);
            dispatch(setUser(response.data.user));
            dispatch(setUser({lists:response.data.lists}));
            console.log("lists;",lists.length);
            return response;
        }catch(err){
            // console.log(err.response.data);
            console.log("era-")
            console.log(err.response);
        };
    }

    return (
        <>
            <div className="flex flex-col">
                <Header />
                <div className="flex flex-col justify-center flex-grow items-center overflow-auto">
                    <Title children="ようこそ" />
                    <SelectList />
                    <AddBtn children="+" onClick={handleAddNewList} />
                    <TestBtn onClick={ () => navigate('/items')} children="itemsへ"/>
                    <TestBtn onClick={ () => navigate('/shoppinglist')} children="listへ"/>
                    <TestBtn onClick={handleFetchUserInfo} children="get" />
                </div>
                <Footer />
            </div>

        </>

    );
}


export default Home;