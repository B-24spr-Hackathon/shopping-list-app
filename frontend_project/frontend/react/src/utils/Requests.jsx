import axios from "axios";

export const FetchUserInfo = async() => {
    try {
        const response = await axios({
            withCredentials: true,
            method: "GET",
            url: 'http://127.0.0.1:8000/api/user/',
        });
        console.log(response);
    } catch (err) {
        console.log('Failure in fetch setup:', err);
    }
};
