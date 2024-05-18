

export async function fetchAndHandleUserInfo(dispatch, navigate) {
    try {
        const userInfo = await fetchUserInfoRequest();
        dispatch(setUser(userInfo.data.user));
        dispatch(setUser({lists: userInfo.data.lists}));

        if (userInfo.data.lists.length === 0) {
            await handleAddNewList();
        } else {
            dispatch(setSelectedList(userInfo.data.lists[userInfo.data.lists.length -1]));
        }

        const newUserInfo = await fetchUserInfoRequest();
        const lastIndex = newUserInfo.data.lists.length - 1;
        const listInfo = await fetchListInfoRequest(newUserInfo.data.lists[lastIndex].list_id);
        dispatch(setSelectedList(listInfo.data));

        const itemsInfo = await fetchItemsOfListRequest(listInfo.data.list_id);
        dispatch(setItemAllInfo(itemsInfo.data.items));

        const shoppingListInfo = await fetchShoppingListRequest(listInfo.data.list_id);
        dispatch(setShoppingItemsAllInfo(shoppingListInfo.data));
    } catch (error) {
        // console.error("Error fetching and handling user information:", error);
    }
}