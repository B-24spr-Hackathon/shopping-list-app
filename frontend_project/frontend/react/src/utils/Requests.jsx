import axios from "axios";
import { useSelector } from "react-redux";

const apiBaseUrl = "https://127.0.0.1:8000/";
export const apiEndpoint = {
    user : "api/user/",
    login: "api/login/",
    list: "api/list/",
    items: "api/items/",
    shoppingList: "api/shopping-list/",
    lineFirst: "api/line/",
    lineLogin: "api/line-login/",
    invite: "api/invite/",
};
// const token = useSelector(state => state.token.token);

export const apiRequest = async({ method, apiEndpoint, data={}, headers={}, withCredentials, token }) => {
    try {
        const response = await axios({
            method: method,
            url: apiBaseUrl + apiEndpoint,
            data: data,
            headers: {
                'Content-Type': 'application/json',
                ...(token && { 'Authorization': `Bearer ${token}` }), // トークンが存在する場合のみ設定
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
export const fetchUserInfoRequest = async(token) => {
    const response = await apiRequest({
        method: 'GET',
        apiEndpoint: apiEndpoint.user,
        withCredentials: true,
        token: token,
    });
    return response;
};


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
            shopping_day: 1,
        },
        withCredentials: true,
    });
    return response;
}
//リスト名を編集するリクエスト
export const editListNameRequest = async( list_id, newValue, token ) => {
    const response = await apiRequest({
        method: 'PATCH',
        apiEndpoint: apiEndpoint.list + list_id + '/',
        data: {
            list_name: newValue,
        },
        withCredentials: true,
        token: token,
    });
    return response;
}
//リストを削除するリクエスト
export const deleteListRequest = async( list_id, token ) => {
    const response = await apiRequest({
        method: 'DELETE',
        apiEndpoint: apiEndpoint.list + list_id + '/',
        withCredentials: true,
        token: token,
    });
    return response;
}
//管理商品リストを取得するリクエスト
export const fetchListInfoRequest = async( list_id ) => {
    const response = await apiRequest({
        method: 'GET',
        apiEndpoint: apiEndpoint.list + list_id + '/',
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
            color: 0,
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
//アイテムを削除するリクエスト
export const deleteItemRequest = async( list_id, item_id ) => {
    const response = await apiRequest({
        method: 'DELETE',
        apiEndpoint: apiEndpoint.items + list_id + "/" + item_id + "/",
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
//招待時にユーザー検索するリクエスト
export const searchFriendRequest = async( user_id, token ) => {
    const response = await apiRequest({
        method: 'GET',
        apiEndpoint: apiEndpoint.invite + user_id + "/",
        withCredentials: true,
        token: token,
    });
    return response;
}
//リストに招待するリクエスト
export const inviteToListRequest = async( list_id, user_id, authority, token ) => {
    const response = await apiRequest({
        method: 'POST',
        apiEndpoint: apiEndpoint.invite,
        data: {
            list_id: list_id,
            user_id: user_id,
            authority: authority
        },
        withCredentials: true,
        token: token,
    });
    return response;
}