import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { setSelectedList } from '../reducers/selectedListSlice';
import { fetchListInfoRequest, fetchItemsOfListRequest, fetchShoppingListRequest } from '../utils/Requests'; // 必要なAPI関数をインポートしてください

function SelectMyList({ lists }) {
    const selectedList = useSelector(state => state.selectedList);
    const token = useSelector(state => state.token.token);
    const dispatch = useDispatch();

    // リストセレクターでリストを変更したときの処理
    const handleSelect = async (listId) => {
        const selected = lists.find(list => list.list_id === listId);
        dispatch(setSelectedList(selected));

        // 選んだリストの情報を取得
        const listInfo = await fetchListInfoRequest(listId, token);
        dispatch(setSelectedList(listInfo.data));

        // 選んだリストの中のアイテムを取得
        // const itemsInfo = await fetchItemsOfListRequest(listId, token);
        // dispatch(setItemAllInfo(itemsInfo.data.items));
        
        // 選んだリストの買い物リストを取得
        // const shoppingListInfo = await fetchShoppingListRequest(listInfo.data.list_id, token);
        // dispatch(setShoppingItemsAllInfo(shoppingListInfo.data));
    };

    return (
        <div className="m-1 hs-dropdown [--trigger:hover] relative inline-flex w-full">
            <button
                id="hs-dropdown-hover-event"
                type="button"
                className="hs-dropdown-toggle w-full py-3 px-4 inline-flex items-center gap-x-2 text-sm font-medium rounded-lg border border-gray-200 bg-white text-gray-800 shadow-sm hover:bg-gray-50 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-white dark:hover:bg-neutral-800"
            >
                {selectedList.list_id ? selectedList.list_name : '選択して下さい'}
                <svg
                    className="hs-dropdown-open:rotate-180 size-4"
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                >
                    <path d="m6 9 6 6 6-6" />
                </svg>
            </button>

            {lists && lists.length > 0 && (
                <div
                    className="hs-dropdown-menu transition-[opacity,margin] duration hs-dropdown-open:opacity-100 opacity-0 hidden min-w-60 bg-white shadow-md rounded-lg p-2 mt-2 dark:bg-neutral-800 dark:border dark:border-neutral-700 dark:divide-neutral-700 after:h-4 after:absolute after:-bottom-4 after:start-0 after:w-full before:h-4 before:absolute before:-top-4 before:start-0 before:w-full"
                    aria-labelledby="hs-dropdown-hover-event"
                >
                    {lists.map((list, index) => (
                        <button
                            key={index}
                            className="flex items-center gap-x-3.5 py-2 px-3 rounded-lg text-sm text-gray-800 hover:bg-gray-100 focus:outline-none focus:bg-gray-100 dark:text-neutral-400 dark:hover:bg-neutral-700 dark:hover:text-neutral-300 dark:focus:bg-neutral-700 w-full text-left"
                            onClick={() => handleSelect(list.list_id)}
                        >
                            {list.list_id} {list.list_name}
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
}

export default SelectMyList;
