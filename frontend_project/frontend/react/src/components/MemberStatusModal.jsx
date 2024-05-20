import React, { useState } from 'react';
import { TestBtn } from './Buttons';

function MemberStatusModal({ member, onApprove, onDecline }) {
    const [isOpen, setIsOpen] = useState(false);

    const friendInvites = member.filter(m => m.member_status === 1 && !m.is_owner);
    const sharedRequests = member.filter(m => m.member_status === 2 && !m.is_owner);
    const myListInvites = member.filter(m => m.member_status === 1 && m.is_owner);
    const myListShares = member.filter(m => m.member_status === 2 && m.is_owner);

    const handleOpen = () => {
        setIsOpen(true);
    };

    const handleClose = () => {
        setIsOpen(false);
    };

    return (
        <>
            <button
                type="button"
                className="py-3 px-4 inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 disabled:pointer-events-none"
                onClick={handleOpen}
            >
                共有
            </button>

            {isOpen && (
                <div className="fixed inset-0 z-50 flex items-center justify-center">
                    {/* オーバーレイ背景 */}
                    <div className="fixed inset-0 bg-black opacity-50 z-40" onClick={handleClose}></div>
                    {/* モーダルコンテンツ */}
                    <div className="relative z-50 sm:max-w-lg sm:w-full m-3 sm:mx-auto">
                        <div className="flex flex-col bg-white border shadow-sm rounded-xl pointer-events-auto dark:bg-neutral-800 dark:border-neutral-700 dark:shadow-neutral-700/70">
                            <div className="flex justify-between items-center py-3 px-4 border-b dark:border-neutral-700">
                                <h3 className="font-bold text-gray-800 dark:text-white">招待・申請の状況</h3>
                                <button
                                    type="button"
                                    className="flex justify-center items-center size-7 text-sm font-semibold rounded-full border border-transparent text-gray-800 hover:bg-gray-100 disabled:opacity-50 disabled:pointer-events-none dark:text-white dark:hover:bg-neutral-700"
                                    onClick={handleClose}
                                >
                                    <span className="sr-only">Close</span>
                                    <svg
                                        className="flex-shrink-0 size-4"
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
                                        <path d="M18 6 6 18"></path>
                                        <path d="m6 6 12 12"></path>
                                    </svg>
                                </button>
                            </div>

                            <div className="flex flex-col border-b">
                                <div className="-m-1.5 overflow-x-auto">
                                    <div className="p-1.5 min-w-full inline-block align-middle">
                                        <div className="overflow-hidden">
                                            <table className="min-w-full divide-y divide-gray-200 dark:divide-neutral-700">
                                                <caption className="py-2 text-center text-large text-gray-600 dark:text-neutral-500">友達からの招待</caption>
                                                <tbody className="divide-y divide-gray-200 dark:divide-neutral-700">
                                                    {friendInvites.length > 0 ? (
                                                        friendInvites.map((m, index) => (
                                                            <tr key={index}>
                                                                <td className="px-6 py-4 text-center whitespace-nowrap text-sm font-medium text-gray-800 dark:text-neutral-200 w-1/4">{m.owner_name}</td>
                                                                <td className="px-6 py-4 text-center whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200 w-1/4">{m.list_name}</td>
                                                                <td className="px-6 py-4 text-center whitespace-nowrap text-sm font-medium w-1/4">
                                                                    <TestBtn children="参加" onClick={() => onApprove(m.member_id)} />
                                                                </td>
                                                                <td className="px-6 py-4 text-center whitespace-nowrap text-sm font-medium w-1/4">
                                                                    <button
                                                                        type="button"
                                                                        onClick={() => onDecline(m.member_id)}
                                                                        className="inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent text-blue-600 hover:text-blue-800 disabled:opacity-50 disabled:pointer-events-none dark:text-blue-500 dark:hover:text-blue-400"
                                                                    >
                                                                        拒否
                                                                    </button>
                                                                </td>
                                                            </tr>
                                                        ))
                                                    ) : (
                                                        <tr>
                                                            <td colSpan="4" className="px-6 py-4 text-center whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200">現在、友達のリストへの招待はありません</td>
                                                        </tr>
                                                    )}
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>
                                </div>

                                <div className="flex flex-col">
                                    <div className="-m-1.5 overflow-x-auto">
                                        <div className="p-1.5 min-w-full inline-block align-middle">
                                            <div className="overflow-hidden">
                                                <table className="min-w-full divide-y divide-gray-200 dark:divide-neutral-700">
                                                    <caption className="py-2 text-center text-large text-gray-600 dark:text-neutral-500">友達のリストへの共有申請</caption>
                                                    <tbody className="divide-y divide-gray-200 dark:divide-neutral-700">
                                                        {sharedRequests.length > 0 ? (
                                                            sharedRequests.map((m, index) => (
                                                                <tr key={index}>
                                                                    <td className="px-6 py-4 text-center whitespace-nowrap text-sm font-medium text-gray-800 dark:text-neutral-200 w-1/4">{m.owner_name}</td>
                                                                    <td className="px-6 py-4 text-center whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200 w-1/4">{m.list_name}</td>
                                                                    <td className="px-6 py-4 text-center whitespace-nowrap text-sm font-medium w-1/4">
                                                                        <button
                                                                            type="button"
                                                                            className="inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent text-blue-600 hover:text-blue-800 disabled:opacity-50 disabled:pointer-events-none dark:text-blue-500 dark:hover:text-blue-400"
                                                                        ></button>
                                                                    </td>
                                                                    <td className="px-6 py-4 text-center whitespace-nowrap text-sm font-medium w-1/4">
                                                                        <button
                                                                            type="button"
                                                                            onClick={() => onDecline(m.member_id)}
                                                                            className="inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent text-blue-600 hover:text-blue-800 disabled:opacity-50 disabled:pointer-events-none dark:text-blue-500 dark:hover:text-blue-400"
                                                                        >
                                                                            中止
                                                                        </button>
                                                                    </td>
                                                                </tr>
                                                            ))
                                                        ) : (
                                                            <tr>
                                                                <td colSpan="4" className="px-6 py-4 text-center whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200">現在、共有申請をしていません</td>
                                                            </tr>
                                                        )}
                                                    </tbody>
                                                </table>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div className="flex flex-col">
                                    <div className="-m-1.5 overflow-x-auto">
                                        <div className="p-1.5 min-w-full inline-block align-middle">
                                            <div className="overflow-hidden">
                                                <table className="min-w-full divide-y divide-gray-200 dark:divide-neutral-700">
                                                    <caption className="py-2 text-center text-large text-gray-600 dark:text-neutral-500">あなたのリストへの招待</caption>
                                                    <tbody className="divide-y divide-gray-200 dark:divide-neutral-700">
                                                        {myListInvites.length > 0 ? (
                                                            myListInvites.map((m, index) => (
                                                                <tr key={index}>
                                                                    <td className="px-6 py-4 text-center whitespace-nowrap text-sm font-medium text-gray-800 dark:text-neutral-200 w-1/4">{m.guest_name}</td>
                                                                    <td className="px-6 py-4 text-center whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200 w-1/4">{m.list_name}</td>
                                                                    <td className="px-6 py-4 text-center whitespace-nowrap text-sm font-medium w-1/4">
                                                                        <button
                                                                            type="button"
                                                                            className="inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent text-blue-600 hover:text-blue-800 disabled:opacity-50 disabled:pointer-events-none dark:text-blue-500 dark:hover:text-blue-400"
                                                                        ></button>
                                                                    </td>
                                                                    <td className="px-6 py-4 text-center whitespace-nowrap text-sm font-medium w-1/4">
                                                                        <button
                                                                            type="button"
                                                                            onClick={() => onDecline(m.member_id)}
                                                                            className="inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent text-blue-600 hover:text-blue-800 disabled:opacity-50 disabled:pointer-events-none dark:text-blue-500 dark:hover:text-blue-400"
                                                                        >
                                                                            中止
                                                                        </button>
                                                                    </td>
                                                                </tr>
                                                            ))
                                                        ) : (
                                                            <tr>
                                                                <td colSpan="4" className="px-6 py-4 text-center whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200">現在、あなたのリストへの招待はありません</td>
                                                            </tr>
                                                        )}
                                                    </tbody>
                                                </table>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div className="flex flex-col">
                                    <div className="-m-1.5 overflow-x-auto">
                                        <div className="p-1.5 min-w-full inline-block align-middle">
                                            <div className="overflow-hidden">
                                                <table className="min-w-full divide-y divide-gray-200 dark:divide-neutral-700">
                                                    <caption className="py-2 text-center text-large text-gray-600 dark:text-neutral-500">あなたのリストへの共有申請</caption>
                                                    <tbody className="divide-y divide-gray-200 dark:divide-neutral-700">
                                                        {myListShares.length > 0 ? (
                                                            myListShares.map((m, index) => (
                                                                <tr key={index}>
                                                                    <td className="px-6 py-4 text-center whitespace-nowrap text-sm font-medium text-gray-800 dark:text-neutral-200 w-1/4">{m.guest_name}</td>
                                                                    <td className="px-6 py-4 text-center whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200 w-1/4">{m.list_name}</td>
                                                                    <td className="px-6 py-4 text-center whitespace-nowrap text-sm font-medium w-1/4">
                                                                        <TestBtn children="承認" onClick={() => onApprove(m.member_id)} />
                                                                    </td>
                                                                    <td className="px-6 py-4 text-center whitespace-nowrap text-sm font-medium w-1/4">
                                                                        <button
                                                                            type="button"
                                                                            onClick={() => onDecline(m.member_id)}
                                                                            className="inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent text-blue-600 hover:text-blue-800 disabled:opacity-50 disabled:pointer-events-none dark:text-blue-500 dark:hover:text-blue-400"
                                                                        >
                                                                            拒否
                                                                        </button>
                                                                    </td>
                                                                </tr>
                                                            ))
                                                        ) : (
                                                            <tr>
                                                                <td colSpan="4" className="px-6 py-4 text-center whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200">現在、共有申請はありません</td>
                                                            </tr>
                                                        )}
                                                    </tbody>
                                                </table>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div className="flex justify-end items-center gap-x-2 py-3 px-4 border-t dark:border-neutral-700">
                                <button
                                    type="button"
                                    className="py-2 px-3 inline-flex items-center gap-x-2 text-sm font-medium rounded-lg border border-gray-200 bg-white text-gray-800 shadow-sm hover:bg-gray-50 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-white dark:hover:bg-neutral-800"
                                    onClick={handleClose}
                                >
                                    Close
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </>
    );
}

export default MemberStatusModal;
