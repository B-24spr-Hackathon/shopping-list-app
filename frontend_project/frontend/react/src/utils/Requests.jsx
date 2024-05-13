import axios from "axios";

const apiBaseUrl = "https://127.0.0.1:8000/";
export const apiEndpoint = {
    user : "api/user/",
    login: "api/login/",
    list: "api/list/",
    items: "api/items/",
};

export const apiRequest = async({ method, apiEndpoint, data={}, headers={}, withCredentials }) => {
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
        return response;
    }catch (err) {
        console.log('Request failed', err);
        throw err;
    }
}
//ユーザー情報を取得のリクエスト
export const fetchUserInfoRequest = async() => {
    const response = await apiRequest({
        method:'GET',
        apiEndpoint: apiEndpoint.user,
        withCredentials: true,
    });
    return response;
}

//ログインのリクエスト
export const loginRequest = async(email, password) => {
    const response = await apiRequest({
        method: 'POST',
        apiEndpoint: apiEndpoint.login,
        data: {
                email: email,
                password: password
            },
        withCredentials: false,
    });
    return response;
}

//新しい管理商品リストを作成するリクエスト
export const addNewListRequest = async() => {
    const response = await apiRequest({
        method: 'POST',
        apiEndpoint: apiEndpoint.list,
        data: {
            list_name: "新しいタイトル",
        },
        withCredentials: true,
    });
    return response;
}

export const fetchItemsOfListRequest = async( list_id ) => {
    const response = await apiRequest({
        method: 'GET',
        apiEndpoint: apiEndpoint.items + list_id + '/',
        withCredentials: true,
    });
    return response;
}


export const updateItemRemindByItemRequest = async( list_id, item_id, newRemindByItem  ) => {
    const response = await apiRequest({
        method: 'PATCH',
        apiEndpoint: apiEndpoint.items + list_id + "/" + item_id + "/",
        data: {
            remind_by_item: newRemindByItem
        },
        withCredentials: true,
    });
    return response;
}

export const updateItemInfoRequest = async( list_id, item_id, key, newItemName  ) => {
    const response = await apiRequest({
        method: 'PATCH',
        apiEndpoint: apiEndpoint.items + list_id + "/" + item_id + "/",
        data: {
            [key]: newItemName
        },
        withCredentials: true,
    });
    return response;
}