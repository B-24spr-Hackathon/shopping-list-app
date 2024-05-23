function ScrollTable(){
    return(
        <>
        <div className='flex justify-center flex-col'>
            <div class="flex flex-col">
                <div class="-m-1.5 overflow-x-auto">
                    <div class="p-1.5 min-w-full inline-block align-middle">
                    <div class="overflow-hidden">
                        <table class="min-w-full divide-y divide-gray-200 dark:divide-neutral-700">
                        <thead>
                            <tr>
                            <th scope="col" class="px-2 py-2 text-center text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">管理する</th>
                            <th colspan="2" scope="col" class="px-2 py-2 text-center text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">商品名</th>
                            <th scope="col" class="px-2 py-2 text-center w-20 text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">消費サイクル</th>
                            <th scope="col" class="px-2 py-2 text-center w-20 text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">直近開封日</th>
                            <th scope="col" class="px-2 py-2 text-center w-16 text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">リンク</th>
                            <th scope="col" class="px-2 py-2 text-center w-20 text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">最終購入日</th>
                            <th scope="col" class="px-2 py-2 text-center w-20 text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">  </th>
                            <th scope="col" class="px-2 py-2 text-center text-xs font-medium text-gray-500 uppercase dark:text-neutral-500">通知する</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-200 dark:divide-neutral-700">
                            <tr>
                            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800 dark:text-neutral-200">John Brown</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200">Regional Paradigm Technician</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200">john@site.com</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200">45</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200">New York No. 1 Lake Park</td>
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
            </div>
        
        
        </>
    )



}

export default ScrollTable;
