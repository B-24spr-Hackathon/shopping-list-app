import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { fetchItemsOfListRequest, fetchListInfoRequest, fetchShoppingListRequest } from "../utils/Requests";
import { useDispatch } from "react-redux";
import { clearSelectedList, setSelectedList } from "../reducers/selectedListSlice";
import { setItemAllInfo, clearItem } from "../reducers/itemSlice.jsx";
import { setShoppingItemsAllInfo } from "../reducers/shoppingItemsSlice.jsx";


function SelectList() {
    const lists = useSelector(state => state.user.lists);
    const selectedList = useSelector(state => state.selectedList)
    const dispatch = useDispatch();
    
    //リストセレクターでリストを変更したとき
    const handleSelectChange = async(event) => {
        const selected = lists.find(list => list.list_id == event.target.value);
        dispatch(setSelectedList(selected));
        //選んだリストの情報を取得
        const listInfo = await fetchListInfoRequest(event.target.value);
        console.log('listinfo', listInfo.data);
        dispatch(setSelectedList(listInfo.data));
        //選んだリストの中のアイテムを取得
        const itemsInfo = await fetchItemsOfListRequest(event.target.value);
        dispatch(setItemAllInfo(itemsInfo.data.items))
        //選んだリストの買い物リストを取得
        const shoppingListInfo = await fetchShoppingListRequest(listInfo.data.list_id);
        //ここでdispatchしたい
        dispatch(setShoppingItemsAllInfo(shoppingListInfo.data.items));

    }

    return (
        <>
            <div>
                <select 
                    value={selectedList.list_id}
                    onChange={handleSelectChange}
                    >
                    {lists.map((list, index) => (
                        <option key={index} value={list.list_id}>
                            {list.list_id} {list.list_name}
                        </option>
                    ))}
                </select>
            </div>
        </>
    );

}

export { SelectList };