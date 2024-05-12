import axios from "axios";

const apiBaseUrl = "https://127.0.0.1:8000/";
export const apiEndpoint = {
    user : "api/user/",
};

export const apiRequest = async( method, apiEndpoint, data, headers, withCredentials ) => {
    try {
        const response = await axios({
            method: method,
            url: apiBaseUrl + apiEndpoint,
            data: data,
            headers: {
                'Content-Type': 'application/json',
                ...headers

            },
            withCredentials:  withCredentials,
        });
        console.log("Response:", response);
        return response.data;
    }catch (err) {
        console.log('Request failed', err);
    }
}