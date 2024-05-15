import axios from "axios";

const apiBaseUrl = "https://127.0.0.1:8000/";
export const apiEndpoint = {
    user : "api/user/",
    login: "api/login/",
    list: "api/list/",
    items: "api/items/",
    shoppingList: "api/shopping-list/",
    lineFirst: "api/line/",
    lineLogin: "api/line-login/",
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
        console.log("apiRequest.Response:", response);
        return response;
    }catch (err) {
        console.log('apiRequest failed', err);
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
export const signUpRequest = async(user_id, user_name, email, password) => {
    const response = await apiRequest({
        method: 'POST',
        apiEndpoint: apiEndpoint.user,
        data: {
                user_id: user_id,
                user_name: user_name,
                email: email,
                password: password,
            },
        withCredentials: false,
    });
    return response;
}
//LINEログイン初回
export const firstLineLoginRequest = async(user_id, user_name, line_id, line_status) => {
    const response = await apiRequest({
        method: 'POST',
        apiEndpoint: apiEndpoint.lineFirst,
        data: {
                user_id: user_id,
                user_name: user_name,
                line_id: line_id,
                line_status: line_status,
            },
        withCredentials: false,
    });
    return response;
}
//LINEログイン2回目以降
export const lineLoginRequest = async(line_id) => {
    const response = await apiRequest({
        method: 'POST',
        apiEndpoint: apiEndpoint.lineLogin,
        data: {
                line_id: line_id,
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
            list_name: "新しいリスト",
        },
        withCredentials: true,
    });
    return response;
}
//新しい商品を追加するリクエスト
export const addNewItemRequest = async( list_id ) => {
    const response = await apiRequest({
        method: 'POST',
        apiEndpoint: apiEndpoint.items + list_id + '/',
        data: {
            item_name: "商品名を入力",
        },
        withCredentials: true,
    });
    return response;
}
//リスト内のアイテムを取得するリクエスト
export const fetchItemsOfListRequest = async( list_id ) => {
    const response = await apiRequest({
        method: 'GET',
        apiEndpoint: apiEndpoint.items + list_id + '/',
        withCredentials: true,
    });
    return response;
}
//アイテムの情報を更新するリクエスト
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
//お買い物リストを取得するリクエスト
export const fetchShoppingListRequest = async( list_id ) => {
    const response = await apiRequest({
        method: 'GET',
        apiEndpoint: apiEndpoint.shoppingList + list_id + "/",
        withCredentials: true,
    });
    return response;
}