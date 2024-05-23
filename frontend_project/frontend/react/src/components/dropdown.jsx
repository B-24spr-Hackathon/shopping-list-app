import React, { useState } from "react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBars } from '@fortawesome/free-solid-svg-icons';
import Select, { components } from 'react-select';
import LogoutButton from "./Logout";
import { TestBtn } from './Buttons';
import { OtherUserNameAndIcon } from "./UserNameIcon";

export const options = [
    { value: 'invite_status', label: "招待・申請の状況" },
    { value: 'logout', label: <LogoutButton /> },
];

const customStyles = {
    control: (provided) => ({
        ...provided,
        minHeight: '30px',
        height: '30px',
        width: '40px', // Smaller width to fit the icon
        backgroundColor: 'transparent',
        border: 'none', // Remove border
        boxShadow: 'none',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center', // Center the icon
        paddingLeft: '0', // Remove padding to center the icon properly
        cursor: 'pointer'
    }),
    valueContainer: (provided) => ({
        ...provided,
        display: 'none' // Hide the value container
    }),
    input: (provided) => ({
        ...provided,
        display: 'none' // Hide the input
    }),
    indicatorsContainer: (provided) => ({
        ...provided,
        height: '30px',
        backgroundColor: 'transparent',
    }),
    option: (provided, state) => ({
        ...provided,
        fontSize: '1.0rem',
        height: '40px',
        backgroundColor: state.isFocused ? 'transparent' : 'transparent', // Remove highlight on select
        color: state.isFocused ? 'black' : 'inherit', // Keep text color as is
        display: 'flex',
        alignItems: 'center',
    }),
    menu: (provided) => ({
        ...provided,
        zIndex: 9999,
        backgroundColor: 'white', // Ensure the menu is visible
        width: '200px', // Ensure the menu is wide enough
        position: 'absolute', // Ensure the menu is positioned absolutely
        right: 0 // Align the right edge of the menu with the right edge of the button
    }),
    menuPortal: (provided) => ({
        ...provided,
        zIndex: 9999,
    }),
    singleValue: (provided) => ({
        ...provided,
        backgroundColor: 'transparent',
    }),
    placeholder: (provided) => ({
        ...provided,
        backgroundColor: 'transparent',
    }),
};

const NoInput = (props) => <components.Input {...props} readOnly />;

const DropdownIndicator = (props) => {
    return (
        <components.DropdownIndicator {...props}>
            <FontAwesomeIcon icon={faBars} style={{ color: 'gray' }} size="2x" />
        </components.DropdownIndicator>
    );
};

const Menu = props => {
    const customMenuStyles = {
        position: 'absolute',
        right: '0', // Align the right edge of the menu with the right edge of the button
    };

    return (
        <div style={customMenuStyles}>
            <components.Menu {...props} />
        </div>
    );
};

const HamburgerSelect = ({ onChange }) => {
    return (
        <Select
            options={options}
            styles={customStyles}
            components={{ DropdownIndicator, IndicatorSeparator: () => null, Input: NoInput, Menu }} // Use custom DropdownIndicator and disable input cursor
            menuPortalTarget={document.body} // Render the menu in the body
            onChange={onChange}
            isClearable={false} // Prevent clearing selected option
        />
    );
};

function NewHamburgerMenu({ member, onApprove, onDecline }) {
    const [isModalOpen, setIsModalOpen] = useState(false);

    const handleMenuSelect = (selectedOption) => {
        if (selectedOption.value === 'invite_status') {
            setIsModalOpen(true);
        } else if (selectedOption.value === 'logout') {
            // ログアウト処理を呼び出す
            console.log("Logging out...");
        }
    };

    const handleModalClose = () => {
        setIsModalOpen(false);
    };

    const friendInvites = member.filter(m => m.member_status === 1 && !m.is_owner);
    const sharedRequests = member.filter(m => m.member_status === 2 && !m.is_owner);
    const myListInvites = member.filter(m => m.member_status === 1 && m.is_owner);
    const myListShares = member.filter(m => m.member_status === 2 && m.is_owner);

    return (
        <>
            <div className="hs-dropdown relative inline-flex">
                <HamburgerSelect onChange={handleMenuSelect} />
            </div>

            {isModalOpen && (
                <div className="fixed inset-0 z-50 flex items-center justify-center">
                    <div className="fixed inset-0 bg-black opacity-50 z-40" onClick={handleModalClose}></div>
                    <div className="relative z-50 w-full max-w-lg sm:max-w-[80%] m-3 sm:mx-auto p-4">
                        <div className="flex flex-col bg-white border shadow-sm rounded-xl pointer-events-auto dark:bg-neutral-800 dark:border-neutral-700 dark:shadow-neutral-700/70">
                            <div className="flex justify-between items-center py-3 px-4 border-b dark:border-neutral-700">
                                <h3 className="font-bold text-gray-800 dark:text-white">招待・申請の状況</h3>
                                <button
                                    type="button"
                                    className="flex justify-center items-center size-7 text-sm font-semibold rounded-full border border-transparent text-gray-800 hover:bg-gray-100 disabled:opacity-50 disabled:pointer-events-none dark:text-white dark:hover:bg-neutral-700"
                                    onClick={handleModalClose}
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
                                                <caption className="py-2 text-center text-lg font-semibold text-gray-800 dark:text-neutral-200">友達からの招待</caption>
                                                <tbody className="divide-y divide-gray-200 dark:divide-neutral-700">
                                                    {friendInvites.length > 0 ? (
                                                        friendInvites.map((m, index) => (
                                                            <tr key={index}>
                                                                <td className="px-2 py-2 text-center whitespace-nowrap text-sm font-medium text-gray-800 dark:text-neutral-200 w-1/4"><OtherUserNameAndIcon userInfo={m.owner_name}/></td>
                                                                <td className="px-2 py-2 text-center whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200 w-1/4">{m.list_name}</td>
                                                                <td className="px-4 py-2 text-center whitespace-nowrap text-sm font-medium w-1/4">
                                                                    <TestBtn children="参加" onClick={() => onApprove(m.member_id)} />
                                                                </td>
                                                                <td className="px-2 py-2 text-center whitespace-nowrap text-sm font-medium w-1/4">
                                                                    <button
                                                                        type="button"
                                                                        onClick={() => onDecline(m.member_id)}
                                                                        className="inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent text-red-600 hover:text-red-400 disabled:opacity-50 disabled:pointer-events-none dark:text-blue-500 dark:hover:text-blue-400"
                                                                    >
                                                                        拒否
                                                                    </button>
                                                                </td>
                                                            </tr>
                                                        ))
                                                    ) : (
                                                        <tr>
                                                            <td colSpan="4" className="px-6 py-4 text-center whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200">現在、友達からの招待はありません</td>
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
                                                    <caption className="py-2 text-center text-lg font-semibold text-gray-800 dark:text-neutral-200">友達のリストへの共有申請</caption>
                                                    <tbody className="divide-y divide-gray-200 dark:divide-neutral-700">
                                                        {sharedRequests.length > 0 ? (
                                                            sharedRequests.map((m, index) => (
                                                                <tr key={index}>
                                                                    <td className="px-2 py-2 text-center whitespace-nowrap text-sm font-medium text-gray-800 dark:text-neutral-200 w-1/4"><OtherUserNameAndIcon userInfo={m.owner_name}/></td>
                                                                    <td className="px-2 py-2 text-center whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200 w-1/4">{m.list_name}</td>
                                                                    <td className="px-4 py-2 text-center whitespace-nowrap text-sm font-medium w-1/4">
                                                                        <button
                                                                            type="button"
                                                                            className="inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent text-blue-600 hover:text-blue-800 disabled:opacity-50 disabled:pointer-events-none dark:text-blue-500 dark:hover:text-blue-400"
                                                                        ></button>
                                                                    </td>
                                                                    <td className="px-2 py-2 text-center whitespace-nowrap text-sm font-medium w-1/4">
                                                                        <button
                                                                            type="button"
                                                                            onClick={() => onDecline(m.member_id)}
                                                                            className="inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent text-red-200 hover:text-red-800 disabled:opacity-50 disabled:pointer-events-none dark:text-blue-500 dark:hover:text-blue-400"
                                                                        >
                                                                            中止
                                                                        </button>
                                                                    </td>
                                                                </tr>
                                                            ))
                                                        ) : (
                                                            <tr>
                                                                <td colSpan="4" className="px-6 py-4 text-center whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200">現在、友達のリストへの共有申請をしていません</td>
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
                                                    <caption className="py-2 text-center text-lg font-semibold text-gray-800 dark:text-neutral-200">自分のリストに招待</caption>
                                                    <tbody className="divide-y divide-gray-200 dark:divide-neutral-700">
                                                        {myListInvites.length > 0 ? (
                                                            myListInvites.map((m, index) => (
                                                                <tr key={index}>
                                                                    <td className="px-2 py-2 text-center whitespace-nowrap text-sm font-medium text-gray-800 dark:text-neutral-200 w-1/4"><OtherUserNameAndIcon userInfo={m.guest_name}/></td>
                                                                    <td className="px-2 py-2 text-center whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200 w-1/4">{m.list_name}</td>
                                                                    <td className="px-4 py-2 text-center whitespace-nowrap text-sm font-medium w-1/4">
                                                                        <button
                                                                            type="button"
                                                                            className="inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent text-blue-600 hover:text-blue-800 disabled:opacity-50 disabled:pointer-events-none dark:text-blue-500 dark:hover:text-blue-400"
                                                                        ></button>
                                                                    </td>
                                                                    <td className="px-2 py-2 text-center whitespace-nowrap text-sm font-medium w-1/4">
                                                                        <button
                                                                            type="button"
                                                                            onClick={() => onDecline(m.member_id)}
                                                                            className="inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent text-red-600 hover:text-red-400 disabled:opacity-50 disabled:pointer-events-none dark:text-blue-500 dark:hover:text-blue-400"
                                                                        >
                                                                            中止
                                                                        </button>
                                                                    </td>
                                                                </tr>
                                                            ))
                                                        ) : (
                                                            <tr>
                                                                <td colSpan="4" className="px-6 py-4 text-center whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200">現在、自分のリストに招待していません</td>
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
                                                    <caption className="py-2 text-center text-lg font-semibold text-gray-800 dark:text-neutral-200">自分のリストの共有申請</caption>
                                                    <tbody className="divide-y divide-gray-200 dark:divide-neutral-700">
                                                        {myListShares.length > 0 ? (
                                                            myListShares.map((m, index) => (
                                                                <tr key={index}>
                                                                    <td className="px-2 py-2 text-center whitespace-nowrap text-sm font-medium text-gray-800 dark:text-neutral-200 w-1/4"><OtherUserNameAndIcon userInfo={m.guest_name}/></td>
                                                                    <td className="px-2 py-2 text-center whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200 w-1/4">{m.list_name}</td>
                                                                    <td className="px-4 py-2 text-center whitespace-nowrap text-sm font-medium w-1/4">
                                                                        <button
                                                                            type="button"
                                                                            className="inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent text-blue-600 hover:text-blue-800 disabled:opacity-50 disabled:pointer-events-none dark:text-blue-500 dark:hover:text-blue-400"
                                                                        ></button>
                                                                    </td>
                                                                    <td className="px-2 py-2 text-center whitespace-nowrap text-sm font-medium w-1/4">
                                                                        <button
                                                                            type="button"
                                                                            onClick={() => onDecline(m.member_id)}
                                                                            className="inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent text-red-600 hover:text-red-400 disabled:opacity-50 disabled:pointer-events-none dark:text-blue-500 dark:hover:text-blue-400"
                                                                        >
                                                                            中止
                                                                        </button>
                                                                    </td>
                                                                </tr>
                                                            ))
                                                        ) : (
                                                            <tr>
                                                                <td colSpan="4" className="px-6 py-4 text-center whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200">現在、自分のリストの共有申請をしていません</td>
                                                            </tr>
                                                        )}
                                                    </tbody>
                                                </table>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div className="py-3 px-4 text-center">
                                <button
                                    type="button"
                                    className="inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent text-blue-600 hover:text-blue-800 disabled:opacity-50 disabled:pointer-events-none dark:text-blue-500 dark:hover:text-blue-400"
                                    onClick={handleModalClose}
                                >
                                    閉じる
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </>
    );
}

export default NewHamburgerMenu;
