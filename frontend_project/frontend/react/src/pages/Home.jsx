import React from "react";
import { useNavigate } from 'react-router-dom';
import { TestBtn } from "../components/Buttons";
import { useSelector } from 'react-redux';
import axios from "axios";
import { useCookies } from 'react-cookie';

function Home() {
    const navigate = useNavigate();
    const user_id = useSelector((state) => state.user.user_id);
    const user_name = useSelector((state) => state.user.user_name);
    const [cookies] = useCookies(['jwt_token']);

    //default_listを更新する処理
    const handleChangeDefault_list = async() => {
        try {
            console.log(cookies);
            const response = await axios.patch('http://127.0.0.1:8000/api/user/', {
                default_list: true
            }, {
                headers: {
                    'Content-Type': 'application/json',
                    // 'Authorization': `Bearer jwt_token=${cookies.jwt_token}`
                    // 'Cookie': `jwt_token=${cookies.jwt_token}`
                    // 'Cookie': `Bearer ${cookies.jwt_token}`
                },
                withCredentials: true
            });
            console.log(response);
            console.log(response.data);

        }catch(err){
            console.log('失敗',err);
        }
    }

    const handleGetRequestTest = async() => {
        try {
            // const response = await axios({
                // withCredentials: true,
                // method: "GET",
                // url: 'http://127.0.0.1:8000/api/user/',
                
            // });
            fetch('http://127.0.0.1:8000/api/user/',{
                method: "GET",
                credentials: 'include'
            })
            // then(response => {
            //     if (!response.ok) {
            //         // サーバーからのレスポンスが成功を示していない場合、エラーを投げる
            //         throw new Error('Network response was not ok: ' + response.statusText);
            //     }
            //     return response.json();
            // })
            // .then(data => {
            //     console.log(data); // 成功したデータ処理
            // })
            // .catch(error => {
            //     console.error('Error during fetch operation:', error); // レスポンス処理またはJSON変換中のエラー
            // });
        } catch (err) {
            console.log('Failure in fetch setup:', err); 
            // console.log(cookies);
            // const response = await axios.get('http://127.0.0.1:8000/api/user/', {
            //     withCredentials: true,
            // });
            // console.log(response);
            // console.log(response.data);

        // }catch(err){
        //     console.log('sippai',err);
        }
    }

    return (
        <>
            <TestBtn onClick={ () => navigate('/items')} children="itemsへ"/>
            <div></div>
            <TestBtn onClick={ () => navigate('/list')} children="listへ"/>
            <div>
                {user_name ? (
                    <p>ようこそ、{user_name}さん（ユーザーID: {user_id}）！</p>
                ) : (
                    <p>ログイン情報がありません。</p>
                )}
            </div>
            <TestBtn onClick={handleChangeDefault_list} children="change" />
            <TestBtn onClick={handleGetRequestTest} children="get" />

        </>

    );
}


export default Home;