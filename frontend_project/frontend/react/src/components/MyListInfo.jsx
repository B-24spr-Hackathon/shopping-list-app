import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEdit, faTrash } from '@fortawesome/free-solid-svg-icons';
import { EditableInputWithButton } from "./EditableDateInput";
import { setSelectedList } from "../reducers/selectedListSlice";
import { editListNameRequest, deleteListRequest, fetchUserInfoRequest, fetchListInfoRequest } from "../utils/Requests";
import { setUser } from "../reducers/userSlice";
import { useNavigate } from 'react-router-dom';

function MemberStatusInfo({ member, token }) {
    return (
        <>

            <div class="flex flex-col border-b">
              <div class="-m-1.5 overflow-x-auto">
                <div class="p-1.5 min-w-full inline-block align-middle">
                  <div class="overflow-hidden">
                    <table class="min-w-full divide-y divide-gray-200 dark:divide-neutral-700">
                      <caption class="py-2 text-center text-sm text-gray-600 dark:text-neutral-500">あなたのリストへの共有リクエストがきています！</caption>
                      <tbody class="divide-y divide-gray-200 dark:divide-neutral-700">
                        <tr>
                          <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800 dark:text-neutral-200">○ユーザー</td>
                          <td class="text-center px-6 py-4 whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200">こちらのリスト</td>
                          <td class="px-6 py-4 whitespace-nowrap text-end text-sm font-medium">
                              <button type="button" class="inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent text-blue-600 hover:text-blue-800 disabled:opacity-50 disabled:pointer-events-none dark:text-blue-500 dark:hover:text-blue-400">承認</button>
                          </td>
                          <td class="px-6 py-4 whitespace-nowrap text-end text-sm font-medium">
                              <button type="button" class="inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent text-blue-600 hover:text-blue-800 disabled:opacity-50 disabled:pointer-events-none dark:text-blue-500 dark:hover:text-blue-400">拒否</button>
                          </td>
                        </tr>
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
                        <caption class="py-2 text-center text-sm text-gray-600 dark:text-neutral-500">共有をリクエストしました。</caption>
                        <tbody class="divide-y divide-gray-200 dark:divide-neutral-700">
                          <tr>
                            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800 dark:text-neutral-200">○ユーザー</td>
                            <td class="text-center px-6 py-4 whitespace-nowrap text-sm text-gray-800 dark:text-neutral-200">相手のリスト名</td>
                            <td class="px-6 py-4 whitespace-nowrap text-end text-sm font-medium">
                                <button type="button" class="inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent text-blue-600 hover:text-blue-800 disabled:opacity-50 disabled:pointer-events-none dark:text-blue-500 dark:hover:text-blue-400">承認まち</button>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-end text-sm font-medium">
                              <button type="button" class="inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent text-blue-600 hover:text-blue-800 disabled:opacity-50 disabled:pointer-events-none dark:text-blue-500 dark:hover:text-blue-400">中止</button>
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
    );
}

export default MemberStatusInfo;
