import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEdit, faTrash } from '@fortawesome/free-solid-svg-icons';
import { EditableInputWithButton } from "./EditableDateInput";
import { setSelectedList } from "../reducers/selectedListSlice";
import { editListNameRequest, deleteListRequest, fetchUserInfoRequest, fetchListInfoRequest } from "../utils/Requests";
import { setUser } from "../reducers/userSlice";
import { useNavigate } from 'react-router-dom';

function MyLists({ lists, token }) {
    const dispatch = useDispatch();
    const selectedList = useSelector(state => state.selectedList);
    const [selectedListId, setSelectedListId] = useState(selectedList.list_id);
    const navigate = useNavigate();

    const handleChange = async (listId) => {
        setSelectedListId(listId);
        const selected = lists.find(list => list.list_id == listId);
        dispatch(setSelectedList(selected));
        // navigate(`/list/${listId}`); // ページ遷移
    };

    const handleEditListName = async (listId, newValue) => {
        const response = await editListNameRequest(listId, newValue, token);
        dispatch(setSelectedList({ ...selectedList, list_name: newValue }));
    };

    const handleDeleteList = async (listId) => {
        const response = await deleteListRequest(listId, token);
        const newUserInfo = await fetchUserInfoRequest(token);
        dispatch(setUser(newUserInfo.data.user));
        if (newUserInfo.data.lists.length > 0) {
            const lastIndex = newUserInfo.data.lists.length - 1;
            const listInfo = await fetchListInfoRequest(newUserInfo.data.lists[lastIndex].list_id, token);
            dispatch(setSelectedList(listInfo.data));
        } else {
            dispatch(setSelectedList(null));
        }
    };

    return (
        <>
            <div>
                {lists.map((list) => (
                    <div className="flex items-center" key={list.list_id}>
                        <input
                            type="radio"
                            name="hs-list-radio"
                            className="shrink-0 mt-0.5 border-gray-200 rounded-full text-blue-600 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-800 dark:border-neutral-700 dark:checked:bg-blue-500 dark:checked:border-blue-500 dark:focus:ring-offset-gray-800"
                            id={`hs-list-radio-${list.list_id}`}
                            value={list.list_id}
                            checked={selectedListId === list.list_id}
                            onChange={() => handleChange(list.list_id)}
                        />
                        <label
                            htmlFor={`hs-list-radio-${list.list_id}`}
                            className="text-sm text-gray-500 ms-2 dark:text-neutral-400 flex-grow"
                        >
                            <EditableInputWithButton
                                initialValue={list.list_name}
                                onSave={(newValue) => handleEditListName(list.list_id, newValue)}
                                onClick={() => handleChange(list.list_id)} // ページ遷移
                                showEditButton={selectedListId === list.list_id} // 編集ボタンの表示条件
                            />
                        </label>
                        {selectedListId === list.list_id && (
                            <>
                                <button onClick={() => handleDeleteList(list.list_id)} className="ml-2">
                                    <FontAwesomeIcon icon={faTrash} />
                                </button>
                            </>
                        )}
                    </div>
                ))}
            </div>
        </>
    );
}

export default MyLists;
