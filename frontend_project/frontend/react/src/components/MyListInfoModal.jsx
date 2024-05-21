import React, { useState } from "react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCircleInfo } from '@fortawesome/free-solid-svg-icons';
import { PermissionDropdownForMyListModal } from "./cmbSelectAuthority";
import { changeEditAuthJoinedListRequest, deleteListRequest, editListInfoRequest, fetchListInfoRequest, fetchUserInfoRequest } from "../utils/Requests";
import { useDispatch, useSelector } from "react-redux";
import { setSelectedList } from "../reducers/selectedListSlice";
import { EditableInput } from "./EditableDateInput";
import { setUser } from "../reducers/userSlice";

function MyListInfoModal() {
    const [isOpen, setIsOpen] = useState(false);
    const token = useSelector(state => state.token.token);
    const list = useSelector(state => state.selectedList)
    const dispatch = useDispatch();

    const handleOpen = () => {
        setIsOpen(true);
    };

    const handleClose = () => {
        setIsOpen(false);
    };

    const handleChangeAuthority = async (memberId, newAuthority) => {
        const formattedAuthority = newAuthority === 'true' ? 'True' : 'False';
        const response = await changeEditAuthJoinedListRequest(memberId, formattedAuthority, token);
        const response1 = await fetchListInfoRequest(list.list_id,token,);
        dispatch(setSelectedList(response1.data));
        console.log(`Response: ${response}`); // デバッグ用に追加
    };

    const handleUpdateListInfo = async(list_id, key, newValue) => {
        const response = await editListInfoRequest(list_id, key, newValue, token);
        const response1 = await fetchListInfoRequest(list.list_id, token);
        dispatch(setSelectedList(response1.data));
    }
    const handleDeleteList = async(list_id) => {
        await deleteListRequest(list_id, token);
        const response = await fetchUserInfoRequest(token);
        dispatch(setUser(response.data));
        handleClose();
    }

    return (
        <>
            <button type="button" className="disabled:opacity-50 disabled:pointer-events-none" onClick={handleOpen}>
                <FontAwesomeIcon icon={faCircleInfo} style={{ color: 'rgba(30, 144, 255,1)' }} size="2x" />
            </button>

            {isOpen && (
                <div className="fixed inset-0 z-50 flex items-center justify-center">
                    {/* オーバーレイ背景 */}
                    <div className="fixed inset-0 bg-black opacity-50 z-40" onClick={handleClose}></div>
                    {/* モーダルコンテンツ */}
                    <div className="relative z-50 sm:max-w-lg sm:w-full m-3 sm:mx-auto">
                        <div className="flex flex-col bg-white border shadow-sm rounded-xl pointer-events-auto dark:bg-neutral-800 dark:border-neutral-700 dark:shadow-neutral-700/70">
                            <div className="flex justify-between items-center py-3 px-4 border-b dark:border-neutral-700">
                                <h3 className="font-bold text-gray-800 dark:text-white">
                                    リスト情報
                                </h3>
                                <button type="button" className="flex justify-center items-center size-7 text-sm font-semibold rounded-full border border-transparent text-gray-800 hover:bg-gray-100 disabled:opacity-50 disabled:pointer-events-none dark:text-white dark:hover:bg-neutral-700" onClick={handleClose}>
                                    <span className="sr-only">Close</span>
                                    <svg className="flex-shrink-0 size-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                        <path d="M18 6 6 18"></path>
                                        <path d="m6 6 12 12"></path>
                                    </svg>
                                </button>
                            </div>
                            <div className="p-4 overflow-y-auto">
                                <p className="mt-1 text-gray-800 dark:text-neutral-400">
                                    リスト名：
                                    {list ? (
                                        <EditableInput
                                            initialValue={list.list_name}
                                            onSave={newValue => handleUpdateListInfo(list.list_id, "list_name", newValue)}
                                        />
                                    ) : (
                                        'No data available'
                                    )}

                                </p>
                                <p className="mt-1 text-gray-800 dark:text-neutral-400">
                                    買い物日：毎月　
                                    {list ? (
                                        <EditableInput
                                            className="text-center w-16"
                                            initialValue={list.shopping_day}
                                            onSave={newValue => handleUpdateListInfo(list.list_id, "shopping_day", newValue)}
                                        />
                                    ) : (
                                        'No data available'
                                    )}
                                    日
                                </p>
                                <p className="mt-1 text-gray-800 dark:text-neutral-400">共有しているユーザー：</p>
                                {list && list.guests_info ? (
                                    list.guests_info.length > 0 ? (
                                        list.guests_info.map((guest, index) => (
                                            <div key={guest.member_id} className="ml-4 text-gray-800 dark:text-neutral-400">
                                                {guest.authority.toString()} {guest.user_name} {guest.member_id}
                                                <PermissionDropdownForMyListModal
                                                    value={guest.authority}
                                                    onChange={(event) => handleChangeAuthority(guest.member_id, event.target.value)}/>
                                            </div>
                                        ))
                                    ) : (
                                        <p className="ml-4 text-gray-800 dark:text-neutral-400">No guests available</p>
                                    )
                                ) : (
                                    <p className="ml-4 text-gray-800 dark:text-neutral-400">No data available</p>
                                )}
                            </div>
                            <div className="flex justify-end items-center gap-x-2 py-3 px-4 border-t dark:border-neutral-700">
                                <button type="button" onClick={() => handleDeleteList(list.list_id)} className="py-2 px-3 inline-flex items-center gap-x-2 text-sm font-medium rounded-lg border border-gray-200 bg-white text-gray-800 shadow-sm hover:bg-gray-50 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-white dark:hover:bg-neutral-800">
                                    削除する
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </>
    );
}

export default MyListInfoModal;