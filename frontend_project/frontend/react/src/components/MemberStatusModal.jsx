import { TestBtn } from "./Buttons";



function MemberStatusModal( { member, onApprove }) {
    const pendingRequests = member.filter(m => m.member_status === 1);
    const sentRequests = member.filter(m => m.member_status === 2);
    const receiveRequests = member.filter(m => m.member_status === 3);

    return (
    <>
        <button type="button" class="py-3 px-4 inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 disabled:pointer-events-none" data-hs-overlay="#hs-slide-up-animation-modal">
            共有
        </button>

        <div id="hs-slide-up-animation-modal" class="hs-overlay hidden size-full fixed top-0 start-0 z-[80] overflow-x-hidden overflow-y-auto pointer-events-none">
            <div class="hs-overlay-open:mt-7 hs-overlay-open:opacity-100 hs-overlay-open:duration-500 mt-14 opacity-0 ease-out transition-all sm:max-w-lg sm:w-full m-3 sm:mx-auto">
                <div class="flex flex-col bg-white border shadow-sm rounded-xl pointer-events-auto dark:bg-neutral-800 dark:border-neutral-700 dark:shadow-neutral-700/70">
                    <div class="flex justify-between items-center py-3 px-4 border-b dark:border-neutral-700">
                        <h3 class="font-bold text-gray-800 dark:text-white">
                            招待・申請の状況
                        </h3>
                        <button type="button" class="hs-dropup-toggle flex justify-center items-center size-7 text-sm font-semibold rounded-full border border-transparent text-gray-800 hover:bg-gray-100 disabled:opacity-50 disabled:pointer-events-none dark:text-white dark:hover:bg-neutral-700" data-hs-overlay="#hs-slide-up-animation-modal">
                            <span class="sr-only">Close</span>
                            <svg class="flex-shrink-0 size-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M18 6 6 18"></path>
                                <path d="m6 6 12 12"></path>
                            </svg>
                        </button>
                    </div>

                    <div class="flex flex-col border-b">
                    <div class="-m-1.5 overflow-x-auto">
                        <div class="p-1.5 min-w-full inline-block align-middle">
                        <div class="overflow-hidden">
                            <table class="min-w-full divide-y divide-gray-200 dark:divide-neutral-700">
                            <caption class="py-2 text-center text-large text-gray-600 dark:text-neutral-500">友達からの招待</caption>
                            <tbody class="divide-y divide-gray-200 dark:divide-neutral-700">
                            {pendingRequests.length > 0 ? (
                                                    pendingRequests.map((m, index) => (
                                        <tr key={index}>
                                            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800 dark:text-neutral-200">{m.owner_name}</td>
                                            <td class="text-center px-6 py-4 whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200">{m.list_name}</td>
                                            <td class="px-6 py-4 whitespace-nowrap text-end text-sm font-medium">
                                                <TestBtn children="参加" onClick={() => onApprove(m.member_id)}/>
                                            </td>
                                            <td class="px-6 py-4 whitespace-nowrap text-end text-sm font-medium">
                                                <TestBtn children="拒否(未実装)"/>
                                            </td>
                                        </tr>
                                    ))
                                ) : (
                                        <tr>
                                            <td colSpan="4" className="px-6 py-4 whitespace-nowrap text-sm text-center text-gray-800 dark:text-neutral-200">現在、友達のリストへの招待はありません</td>
                                        </tr>
                                )}
                            </tbody>
                            </table>
                        </div>
                        </div>
                    </div>

                    <div class="flex flex-col">
                        <div class="-m-1.5 overflow-x-auto">
                        <div class="p-1.5 min-w-full inline-block align-middle">
                            <div class="overflow-hidden">
                            <table class="min-w-full divide-y divide-gray-200 dark:divide-neutral-700">
                                <caption class="py-2 text-center text-large text-gray-600 dark:text-neutral-500">友達のリストへの共有申請</caption>
                                <tbody class="divide-y divide-gray-200 dark:divide-neutral-700">
                                {sentRequests.length > 0 ? (
                                                        sentRequests.map((m, index) => (
                                            <tr key={index}>
                                                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800 dark:text-neutral-200">{m.owner_name}</td>
                                                <td class="text-center px-6 py-4 whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200">{m.list_name}</td>
                                                <td class="px-6 py-4 whitespace-nowrap text-end text-sm font-medium">
                                                    <button type="button" class="inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent text-blue-600 hover:text-blue-800 disabled:opacity-50 disabled:pointer-events-none dark:text-blue-500 dark:hover:text-blue-400"></button>
                                                </td>
                                                <td class="px-6 py-4 whitespace-nowrap text-end text-sm font-medium">
                                                <button type="button" class="inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent text-blue-600 hover:text-blue-800 disabled:opacity-50 disabled:pointer-events-none dark:text-blue-500 dark:hover:text-blue-400">中止(未実装)</button>
                                                </td>
                                            </tr>
                                        ))
                                    ) : (
                                            <tr>
                                                <td colSpan="4" className="px-6 py-4 whitespace-nowrap text-sm text-center text-gray-800 dark:text-neutral-200">現在、共有申請をしていません</td>
                                            </tr>
                                    )}
                                </tbody>
                            </table>
                            </div>
                        </div>
                        </div>
                    </div>
                    </div>
                    <div class="flex flex-col">
                        <div class="-m-1.5 overflow-x-auto">
                        <div class="p-1.5 min-w-full inline-block align-middle">
                            <div class="overflow-hidden">
                            <table class="min-w-full divide-y divide-gray-200 dark:divide-neutral-700">
                                <caption class="py-2 text-center text-large text-gray-600 dark:text-neutral-500">あなたのリストへの共有申請</caption>
                                <tbody class="divide-y divide-gray-200 dark:divide-neutral-700">
                                {receiveRequests.length > 0 ? (
                                                        receiveRequests.map((m, index) => (
                                            <tr key={index}>
                                                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800 dark:text-neutral-200">{m.owner_name}</td>
                                                <td class="text-center px-6 py-4 whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200">{m.list_name}</td>
                                                <td class="px-6 py-4 whitespace-nowrap text-end text-sm font-medium">
                                                    <button type="button" class="inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent text-blue-600 hover:text-blue-800 disabled:opacity-50 disabled:pointer-events-none dark:text-blue-500 dark:hover:text-blue-400">承認まち</button>
                                                </td>
                                                <td class="px-6 py-4 whitespace-nowrap text-end text-sm font-medium">
                                                <button type="button" class="inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent text-blue-600 hover:text-blue-800 disabled:opacity-50 disabled:pointer-events-none dark:text-blue-500 dark:hover:text-blue-400">中止</button>
                                                </td>
                                            </tr>
                                        ))
                                    ) : (
                                            <tr>
                                                <td colSpan="4" className="px-6 py-4 whitespace-nowrap text-sm text-center text-gray-800 dark:text-neutral-200">現在、共有申請はありません。</td>
                                            </tr>
                                    )}
                                </tbody>
                            </table>
                            </div>
                        </div>
                        </div>
                    </div>
                    

                    <div class="flex justify-end items-center gap-x-2 py-3 px-4 border-t dark:border-neutral-700">
                        <button type="button" class="hs-dropup-toggle py-2 px-3 inline-flex items-center gap-x-2 text-sm font-medium rounded-lg border border-gray-200 bg-white text-gray-800 shadow-sm hover:bg-gray-50 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-900 dark:border-neutral-700 dark:text-white dark:hover:bg-neutral-800" data-hs-overlay="#hs-slide-up-animation-modal">
                            Close
                        </button>
                        {/* <button type="button" class="py-2 px-3 inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 disabled:pointer-events-none">
                            Save changes
                        </button> */}
                    </div>
                </div>
            </div>
        </div>
    </>
    );
};

export default MemberStatusModal;