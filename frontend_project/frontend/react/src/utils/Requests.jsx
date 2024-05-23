import axios from "axios";
import { useSelector } from "react-redux";

const apiBaseUrl = "https://alb.tech-talk-cloud.net/";
export const apiEndpoint = {
    user : "api/user/",
    login: "api/login/",
    list: "api/list/",
    items: "api/items/",
    shoppingList: "api/shopping-list/",
    lineFirst: "api/line/",
    lineLogin: "api/line-login/",
    lineLink: 'api/line-link/',
    invite: "api/invite/",
    apply: "api/apply/",
    member_status: "api/member_status/",
    entry: "api/entry/",
    accept: "api/entry/accept/",
    decline: "api/entry/decline/",
};

export const lineUrl = "https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id=2004751038&redirect_uri=https%3A%2F%2Falb.tech-talk-cloud.net%2Fapi%2Fcallback%2F&state=shopping-list12345&bot_prompt=aggressive&scope=profile%20openid";


const apiRequest = async({ method, apiEndpoint, data={}, headers={}, withCredentials, token }) => {
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
//共有の招待・申請状況を取得するリクエスト
export const fetchMemberStatusInfoRequest = async(token) => {
    const response = await apiRequest({
        method: 'GET',
        apiEndpoint: apiEndpoint.member_status,
        withCredentials: true,
        token: token,
    });
    return response;
};


//ユーザー情報を更新するリクエスト
export const updateUserInfoRequest = async( key, newValue, token  ) => {
    const response = await apiRequest({
        method: 'PATCH',
        apiEndpoint: apiEndpoint.user,
        data: {
            [key]: newValue
        },
        withCredentials: true,
        token: token,
    });
    return response;
}
//退会のリクエスト
export const dropUserRequest = async(token) => {
    const response = await apiRequest({
        method: 'DELETE',
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
//新規登録のリクエスト
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
//LINE連携
export const lineLinkRequest = async(token) => {
    const response = await apiRequest({
        method: 'GET',
        apiEndpoint: apiEndpoint.lineLink,
        withCredentials: true,
        toke: token,
    });
    return response;
}

//新しい管理商品リストを作成するリクエスト
export const addNewListRequest = async(token) => {
    const response = await apiRequest({
        method: 'POST',
        apiEndpoint: apiEndpoint.list,
        data: {
            list_name: "新しいリスト",
            shopping_day: 1,
        },
        withCredentials: true,
        token: token,
    });
    return response;
}
//リスト名を編集するリクエスト
export const editListInfoRequest = async( list_id, key, newValue, token ) => {
    const response = await apiRequest({
        method: 'PATCH',
        apiEndpoint: apiEndpoint.list + list_id + '/',
        data: {
            [key]: newValue,
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
export const fetchListInfoRequest = async( list_id, token ) => {
    const response = await apiRequest({
        method: 'GET',
        apiEndpoint: apiEndpoint.list + list_id + '/',
        withCredentials: true,
        token: token,
    });
    return response;
}

//新しい商品を追加するリクエスト
export const addNewItemRequest = async( list_id, token ) => {
    const response = await apiRequest({
        method: 'POST',
        apiEndpoint: apiEndpoint.items + list_id + '/',
        data: {
            color: 0,
            item_name: "商品名を入力",
        },
        withCredentials: true,
        token: token,
    });
    return response;
}
//リスト内のアイテムを取得するリクエスト
export const fetchItemsOfListRequest = async( list_id, token ) => {
    const response = await apiRequest({
        method: 'GET',
        apiEndpoint: apiEndpoint.items + list_id + '/',
        withCredentials: true,
        token: token,
    });
    return response;
}
//アイテムの情報を更新するリクエスト
export const updateItemInfoRequest = async( list_id, item_id, key, newItemName, token  ) => {
    const response = await apiRequest({
        method: 'PATCH',
        apiEndpoint: apiEndpoint.items + list_id + "/" + item_id + "/",
        data: {
            [key]: newItemName
        },
        withCredentials: true,
        token: token,
    });
    return response;
}
//アイテムを削除するリクエスト
export const deleteItemRequest = async( list_id, item_id, token ) => {
    const response = await apiRequest({
        method: 'DELETE',
        apiEndpoint: apiEndpoint.items + list_id + "/" + item_id + "/",
        withCredentials: true,
        token: token,
    });
    return response;
}
//お買い物リストを取得するリクエスト
export const fetchShoppingListRequest = async( list_id, token ) => {
    const response = await apiRequest({
        method: 'GET',
        apiEndpoint: apiEndpoint.shoppingList + list_id + "/",
        withCredentials: true,
        token: token,
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

//共有申請時にユーザー検索するリクエスト
export const searchApplyFriendRequest = async( user_id, token ) => {
    const response = await apiRequest({
        method: 'GET',
        apiEndpoint: apiEndpoint.apply + user_id + "/",
        withCredentials: true,
        token: token,
    });
    console.log("");
    return response;
}

//リストの共有を申請するリクエスト
export const applyToListRequest = async( list_id, user_id, authority, token ) => {
    const response = await apiRequest({
        method: 'POST',
        apiEndpoint: apiEndpoint.apply,
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
//リストの共有を許可するリクエスト(招待も申請も共通)
export const approveToListRequest = async( member_id, token ) => {
    const response = await apiRequest({
        method: 'PATCH',
        apiEndpoint: apiEndpoint.accept + member_id + '/',
        data: {
            member_status: 0,
        },
        withCredentials: true,
        token: token,
    });
    return response;
}
//自分からのリストの招待、申請、友達からの申請を拒否するリクエスト
export const declineToListRequest = async( member_id, token ) => {
    const response = await apiRequest({
        method: 'DELETE',
        apiEndpoint: apiEndpoint.decline + member_id + '/',
        withCredentials: true,
        token: token,
    });
    return response;
}
//共有リストの権限変更（招待・申請共通）
export const changeEditAuthJoinedListRequest = async( member_id, authority, token ) => {
    const response = await apiRequest({
        method: 'PATCH',
        apiEndpoint: apiEndpoint.entry + member_id + '/',
        data: {
            authority: authority,
        },
        withCredentials: true,
        token: token,
    });
    return response;
}
//共有リストの共有解除（招待・申請共通）
export const removeJoinedListRequest = async( member_id, token ) => {
    const response = await apiRequest({
        method: 'DELETE',
        apiEndpoint: apiEndpoint.entry + member_id + '/',
        withCredentials: true,
        token: token,
    });
    return response;
}

