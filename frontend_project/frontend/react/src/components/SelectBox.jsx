import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { fetchItemsOfListRequest, fetchListInfoRequest, fetchShoppingListRequest, fetchUserInfoRequest } from "../utils/Requests";
import { useDispatch } from "react-redux";
import { clearSelectedList, setSelectedList } from "../reducers/selectedListSlice";
import { setItemAllInfo } from "../reducers/itemSlice.jsx";
import { setShoppingItemsAllInfo } from "../reducers/shoppingItemsSlice.jsx";


function SelectList() {
    const selectedList = useSelector(state => state.selectedList)

    const dispatch = useDispatch();
    const [lists, setLists] = useState([]);

    useEffect(() => {
        const fetchLists = async() => {
            const response = await fetchUserInfoRequest();
            setLists(response.data.lists);
            console.log('res',response.data.lists);
        };
        fetchLists();
    },[]);

    
    
    //リストセレクターでリストを変更したとき
    const handleSelectChange = async(event) => {
        const selected = lists.find(list => list.list_id == event.target.value);
        dispatch(setSelectedList(selected));
        //選んだリストの情報を取得
        const listInfo = await fetchListInfoRequest(event.target.value);
        dispatch(setSelectedList(listInfo.data));
        //選んだリストの中のアイテムを取得
        const itemsInfo = await fetchItemsOfListRequest(event.target.value);
        // dispatch(setItemAllInfo(itemsInfo.data.items))
        //選んだリストの買い物リストを取得
        const shoppingListInfo = await fetchShoppingListRequest(listInfo.data.list_id);
        // dispatch(setShoppingItemsAllInfo(shoppingListInfo.data));

    }

    return (
        <>
            <label for="hs-hidden-select" class="sr-only">Label</label>
            <select
                value={selectedList.list_id}
                onChange={handleSelectChange}
                id="hs-hidden-select"
                class="py-3 px-4 pe-9 block w-auto border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-neutral-400 dark:placeholder-neutral-500 dark:focus:ring-neutral-600">
                {/* <option selected="">あなたのリスト</option> */}
                {lists.map((list, index) => (
                    <option key={index} value={list.list_id}>
                            {list.list_id} {list.list_name}
                    </option>
                    ))}
            </select>
        </>
    );

}
function ForInviteSelectList({ onSelectChange }) {
    const [selectedListId, setSelectedListId] = useState('');
    const [lists, setLists] = useState([]);

    useEffect(() => {
        const fetchLists = async () => {
            const response = await fetchUserInfoRequest();
            setLists(response.data.lists);
            console.log('res', response.data.lists);
        };
        fetchLists();
    }, []);

    // リストセレクターでリストを変更したとき
    const handleSelectChange = async (event) => {
        const selectedId = event.target.value;
        setSelectedListId(selectedId);
        const selected = lists.find(list => list.list_id == selectedId);
        if (onSelectChange) {
            onSelectChange(selected.list_id);
        }

        // //選んだリストの情報を取得
        // const listInfo = await fetchListInfoRequest(selectedId);
        // // dispatch(setSelectedList(listInfo.data));
        // //選んだリストの中のアイテムを取得
        // const itemsInfo = await fetchItemsOfListRequest(selectedId);
        // // dispatch(setItemAllInfo(itemsInfo.data.items))
        // //選んだリストの買い物リストを取得
        // const shoppingListInfo = await fetchShoppingListRequest(listInfo.data.list_id);
        // // dispatch(setShoppingItemsAllInfo(shoppingListInfo.data));
    }

    return (
        <>
            <label htmlFor="hs-hidden-select" className="sr-only">Label</label>
            <select
                value={selectedListId}
                onChange={handleSelectChange}
                id="hs-hidden-select"
                className="py-3 px-4 pe-9 block w-auto border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-neutral-400 dark:placeholder-neutral-500 dark:focus:ring-neutral-600">
                <option value="" disabled>招待するリストを選択</option>
                {lists.map((list, index) => (
                    <option key={index} value={list.list_id}>
                        {list.list_id} {list.list_name}
                    </option>
                ))}
            </select>
        </>
    );
}

export { SelectList, ForInviteSelectList };


