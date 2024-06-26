import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { fetchItemsOfListRequest, fetchListInfoRequest, fetchShoppingListRequest, fetchUserInfoRequest } from "../utils/Requests";
import { useDispatch } from "react-redux";
import { clearSelectedList, setSelectedList } from "../reducers/selectedListSlice";

//homeのリストセレクター
function SelectList({lists}) {
    const selectedList = useSelector(state => state.selectedList);
    const token = useSelector(state => state.token.token);
    const dispatch = useDispatch();

    //リストセレクターでリストを変更したとき
    const handleSelectChange = async(event) => {
        const selected = lists.find(list => list.list_id == event.target.value);
        dispatch(setSelectedList(selected));
        //リストのオーナーならば
        if(selected.is_owner){
            //選んだリストの情報を取得
            const listInfo = await fetchListInfoRequest(event.target.value, token);
            dispatch(setSelectedList(listInfo.data));
        }
    }
    return (
        <>
            <label for="hs-hidden-select" className="sr-only ">Label</label>
            <select
                value={selectedList.list_id}
                onChange={handleSelectChange}
                id="hs-hidden-select"
                class="py-3 px-4 pe-9 block w-full text-center border-gray-200 border rounded-lg text-l focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none">
                {/* <option selected="">あなたのリスト</option> */}
                {lists.map((list, index) => (
                    <option key={index} value={list.list_id}>
                        {list.list_name}
                    </option>
                    ))}
            </select>
        </>
    );
}
//shoppingListのリストセレクター
function ForShoppingListSelectList({lists}) {
    const selectedList = useSelector(state => state.selectedList);
    const token = useSelector(state => state.token.token);
    const dispatch = useDispatch();

    //リストセレクターでリストを変更したとき
    const handleSelectChange = async(event) => {
        const selected = lists.find(list => list.list_id == event.target.value);
        dispatch(setSelectedList(selected));
        //リストのオーナーならば
        // if(selectedList.is_owner){
        //     //選んだリストの情報を取得
        //     const itemsInfo = await fetchItemsOfListRequest(event.target.value, token);
        //     // dispatch(setSelectedList(listInfo.data));
        
        // }else if (selectedList.authority){
        //     //選んだリストの中のアイテムを取得
        //     const itemsInfo = await fetchItemsOfListRequest(event.target.value, token);
        //     // dispatch(setItemAllInfo(itemsInfo.data.items))
        // }
        // //選んだリストの買い物リストを取得
        // const shoppingListInfo = await fetchShoppingListRequest(selectedList.list_id, token);
        // // dispatch(setShoppingItemsAllInfo(shoppingListInfo.data));
    }
    return (
        <>
            <label for="hs-hidden-select" className="sr-only ">Label</label>
            <select
                value={selectedList.list_id}
                onChange={handleSelectChange}
                id="hs-hidden-select"
                class="py-3 px-4 pe-9 block w-full text-center border-gray-200 border rounded-lg text-l focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none">
                {/* <option selected="">あなたのリスト</option> */}
                {lists.map((list, index) => (
                    <option key={index} value={list.list_id}>
                        {list.list_name}
                    </option>
                    ))}
            </select>
        </>
    );
}



//招待リスト用のセレクター
function ForInviteSelectList({ onSelectChange, lists }) {
    const [selectedListId, setSelectedListId] = useState('');

    // リストセレクターでリストを変更したとき
    const handleSelectChange = async (event) => {
        const selectedId = event.target.value;
        setSelectedListId(selectedId);
        const selected = lists.find(list => list.list_id == selectedId);
        if (onSelectChange) {
            onSelectChange(selected.list_id);
        }
    }
    return (
        <>
            <label htmlFor="hs-hidden-select" className="sr-only">Label</label>
            <select
                value={selectedListId}
                onChange={handleSelectChange}
                id="hs-hidden-select"
                className="py-3 px-4 pe-9 block w-auto border border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none">
                <option value="" disabled>招待するリストを選択</option>
                {lists.map((list, index) => (
                    <option key={index} value={list.list_id}>
                        {list.list_name}
                    </option>
                ))}
            </select>
        </>
    );
}
//申請リスト用のセレクター
function ForApplySelectList({ onSelectChange, lists }) {
    const [selectedApplyListId, setSelectedApplyListId] = useState('');

    // リストセレクターでリストを変更したとき
    const handleSelectChange = async (event) => {
        const selectedId = event.target.value;
        setSelectedApplyListId(selectedId);
        const selected = lists.find(list => list.list_id == selectedId);
        if (onSelectChange) {
            onSelectChange(selected.list_id);
        }
    }

    return (
        <>
            <label htmlFor="hs-hidden-select " className="sr-only">Label</label>
            <select
                value={selectedApplyListId}
                onChange={handleSelectChange}
                id="hs-hidden-select"
                className="py-3 px-4 pe-9 border block w-auto border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none">
                <option value="" disabled>申請するリストを選択</option>
                {lists.map((list, index) => (
                    <option key={index} value={list.list_id}>
                        {list.list_name}
                    </option>
                ))}
            </select>
        </>
    );
}

export { SelectList, ForShoppingListSelectList, ForInviteSelectList, ForApplySelectList };


