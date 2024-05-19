import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEdit, faTrash } from '@fortawesome/free-solid-svg-icons';
import { EditableInputWithButton } from "./EditableDateInput";
import { setSelectedList } from "../reducers/selectedListSlice";
import { editListNameRequest, deleteListRequest, fetchUserInfoRequest, fetchListInfoRequest } from "../utils/Requests";
import { setUser } from "../reducers/userSlice";
import { useNavigate } from 'react-router-dom';

function MyListInfo({ lists, token }) {
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

            <div class="flex flex-col border-b">
              <div class="-m-1.5 overflow-x-auto">
                <div class="p-1.5 min-w-full inline-block align-middle">
                  <div class="overflow-hidden">
                    <table class="min-w-full divide-y divide-gray-200 dark:divide-neutral-700">
                      <caption class="py-2 text-center text-sm text-gray-600 dark:text-neutral-500">選択したリスト</caption>
                      {/* <thead>
                        <tr>
                          <th scope="col" class="px-6 py-3 text-start text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">Name</th>
                          <th scope="col" class="px-6 py-3 text-start text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">Age</th>
                          <th scope="col" class="px-6 py-3 text-start text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">Address</th>
                          <th scope="col" class="px-6 py-3 text-end text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">Action</th>
                        </tr>
                      </thead> */}
                      <tbody class="divide-y divide-gray-200 dark:divide-neutral-700">
                        <tr>
                          <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800 dark:text-neutral-200">リスト名</td>
                          <td class="text-center px-6 py-4 whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200">New York No. 1 Lake Park</td>
                          
                        </tr>
                        

                        <tr>
                          <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800 dark:text-neutral-200">買い物日</td>
                          <td class="text-center px-6 py-4 whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200">毎月27</td>
                        </tr>

                        {/* <tr>
                          <td colSpan='4' class="text-center px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800 dark:text-neutral-200">共有しているユーザー</td>
                          
                        </tr>
                        <tr>
                          <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800 dark:text-neutral-200">Joe Black</td>
                          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200">31</td>
                          <td class="px-6 py-4 whitespace-nowrap text-end text-sm font-medium">
                            <button type="button" class="inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent text-blue-600 hover:text-blue-800 disabled:opacity-50 disabled:pointer-events-none dark:text-blue-500 dark:hover:text-blue-400">Delete</button>
                          </td>
                        </tr> */}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>

            <div class="flex flex-col">
              <div class="-m-1.5 overflow-x-auto">
                <div class="p-1.5 min-w-full inline-block align-middle">
                  <div class="overflow-hidden">
                    <table class="min-w-full divide-y divide-gray-200 dark:divide-neutral-700">
                      <caption class="py-2 text-center text-sm text-gray-600 dark:text-neutral-500">共有しているユーザー</caption>
                      {/* <thead>
                        <tr>
                          <th scope="col" class="px-6 py-3 text-start text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">Name</th>
                          <th scope="col" class="px-6 py-3 text-start text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">Age</th>
                          <th scope="col" class="px-6 py-3 text-start text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">Address</th>
                          <th scope="col" class="px-6 py-3 text-end text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">Action</th>
                        </tr>
                      </thead> */}
                      <tbody class="divide-y divide-gray-200 dark:divide-neutral-700">
                        <tr>
                          <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800 dark:text-neutral-200">Joe Blackdsfdasdafdsdaf</td>
                          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200">31</td>
                          <td class="px-6 py-4 whitespace-nowrap text-end text-sm font-medium">
                            <button type="button" class="inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent text-blue-600 hover:text-blue-800 disabled:opacity-50 disabled:pointer-events-none dark:text-blue-500 dark:hover:text-blue-400">Delete</button>
                          </td>
                        </tr>
                        <tr>
                          <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800 dark:text-neutral-200">Joe Blackdsfdasdafdsdaf</td>
                          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200">31</td>
                          <td class="px-6 py-4 whitespace-nowrap text-end text-sm font-medium">
                            <button type="button" class="inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent text-blue-600 hover:text-blue-800 disabled:opacity-50 disabled:pointer-events-none dark:text-blue-500 dark:hover:text-blue-400">Delete</button>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>

        </>
    );
}

export default MyListInfo;
