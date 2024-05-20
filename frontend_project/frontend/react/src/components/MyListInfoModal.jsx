import React from "react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCircleInfo } from '@fortawesome/free-solid-svg-icons';

function MyListInfoModal({ list }) {
    return (
        <>
            <button type="button" className="disabled:opacity-50 disabled:pointer-events-none" data-hs-overlay="#hs-basic-modal">
                <FontAwesomeIcon icon={faCircleInfo} style={{ color: 'rgba(185, 50, 0, 1)' }} />
            </button>

            <div id="hs-basic-modal" className="hs-overlay hs-overlay-open:opacity-100 hs-overlay-open:duration-500 hidden fixed inset-0 z-[80] opacity-0 transition-all pointer-events-none flex items-center justify-center">
                {/* オーバーレイ背景 */}
                <div className="fixed inset-0 bg-black opacity-50"></div>
                {/* モーダルコンテンツ */}
                <div className="relative z-10 sm:max-w-lg sm:w-full m-3 sm:mx-auto">
                    <div className="flex flex-col bg-white border shadow-sm rounded-xl pointer-events-auto dark:bg-neutral-800 dark:border-neutral-700 dark:shadow-neutral-700/70">
                        {/* <div className="flex justify-between items-center py-3 px-4 border-b dark:border-neutral-700">
                            <h3 className="font-bold text-gray-800 dark:text-white">
                                Modal title
                            </h3>
                            <button type="button" className="flex justify-center items-center size-7 text-sm font-semibold rounded-full border border-transparent text-gray-800 hover:bg-gray-100 disabled:opacity-50 disabled:pointer-events-none dark:text-white dark:hover:bg-neutral-700" data-hs-overlay="#hs-basic-modal">
                                <span className="sr-only">Close</span>
                                <svg className="flex-shrink-0 size-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                    <path d="M18 6 6 18"></path>
                                    <path d="m6 6 12 12"></path>
                                </svg>
                            </button>
                        </div> */}
                        <div className="p-4 overflow-y-auto">
                            <p className="mt-1 text-gray-800 dark:text-neutral-400">
                                リスト名：{list ? list.list_name : 'No data available'}
                                買い物日：{list ? list.shopping_day : 'No data available'}
                            </p>
                            <p>共有しているユーザー</p>
                            {list && list.guests_info ? (
                                    list.guests_info.length > 0 ? (
                                        list.guests_info.map((guest, index) => (
                                            <p key={index} className="ml-4 text-gray-800 dark:text-neutral-400">{guest.user_name}</p>
                                        ))
                                    ) : (
                                        <p className="ml-4 text-gray-800 dark:text-neutral-400">No guests available</p>
                                    )
                                ) : (
                                    <p className="ml-4 text-gray-800 dark:text-neutral-400">No data available</p>
                                )}
                        </div>
                        <div className="flex justify-end items-center gap-x-2 py-3 px-4 border-t dark:border-neutral-700">
                            <button type="button" className="py-2 px-3 inline-flex items-center gap-x-2 text-sm font-medium rounded-lg border border-gray-200 bg-white text-gray-800 shadow-sm hover:bg-gray-50 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-white dark:hover:bg-neutral-800" data-hs-overlay="#hs-basic-modal">
                                Close
                            </button>
                            <button type="button" className="py-2 px-3 inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 disabled:pointer-events-none">
                                Save changes
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
}

export default MyListInfoModal;
