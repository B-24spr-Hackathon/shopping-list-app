import React, { useEffect, useRef, useState }  from 'react';
import '../styles/Lists.css'
import { AddBtn, BoughtOrPassBtn, ShoppingBtn, ToShoppingListBtn } from './Buttons';
import { useDispatch, useSelector } from 'react-redux';
import { addNewItemRequest, deleteItemRequest, fetchItemsOfListRequest, fetchListInfoRequest, fetchShoppingListRequest, updateItemInfoRequest } from '../utils/Requests';
import { setItemAllInfo, updateColor, updateConsumeCycle, updateItemName, updateItemUrl, updateLastOpenAt, updateLastPurchaseAt, updateManageTarget, updateRemindByItem, updateToList, deleteItem } from '../reducers/itemSlice';
import "../styles/CategoryColor.css";
import { setShoppingItemsAllInfo } from '../reducers/shoppingItemsSlice';
import { EditableDateInput, EditableInput } from './EditableDateInput';
import { TrashBtn } from './trashicon';
import reactSelect from "react-select";
import SimpleSelectBox from './SimpleReactSelect';
import { options } from './SimpleReactSelect';
import { setSelectedList } from '../reducers/selectedListSlice';


//買い物リスト画面のパネル
function ShoppingListPanel() {
    const selectedList = useSelector(state => state.selectedList);
    // const shoppingItems = useSelector(state => state.shoppingItems)
    const items = useSelector(state => state.shoppingItems.items);
    const dispatch = useDispatch();
    const [shoppingItems, setShoppingItems] = useState([]);
    const [ShoppingListInfo, setShoppingListInfo] = useState([]);
    const token = useSelector(state => state.token.token);


    //読み込み時にshoppingItemデータを取得
    useEffect(() => {
        const fetchShoppingList = async() => {
            const shoppingListResponse = await fetchShoppingListRequest(selectedList.list_id, token);
            setShoppingItems(shoppingListResponse.data.items);
            setShoppingListInfo(shoppingListResponse.data);
        }
        fetchShoppingList();
    },[selectedList]);

    //見送りボタン（買い物リストから外す）
    const handlePass = async(item) => {
        try {
            await updateItemInfoRequest(selectedList.list_id, item.item_id, "to_list", false, token);
            // dispatch(updateToList({ item_id: item.item_id, to_list: response.data.to_list }));
            const response = await fetchShoppingListRequest(selectedList.list_id, token);
            setShoppingItems(response.data.items);
            setShoppingListInfo(response.data);
            // console.log(currentShoppingList.data);
            // dispatch(setShoppingItemsAllInfo(currentShoppingList.data));
        }catch (err){
            console.error('Failed to update manage target:', err);
        }
    }
    //買ったボタン（買い物リストから外す・購入日を今日にする）
    const handleBought = async(item) => {
        try{
            await updateItemInfoRequest(selectedList.list_id, item.item_id, "to_list", false, token);
            const today = new Date();
            const formattedDate = today.toISOString().slice(0, 10);
            await updateItemInfoRequest(selectedList.list_id, item.item_id, "last_purchase_at", formattedDate, token);
            const response = await fetchShoppingListRequest(selectedList.list_id, token);
            setShoppingItems(response.data.items);


        }catch (err){
            console.error('Failed to update manage target:', err);
        }
    }

    // カテゴリカラーアイコンを取得する関数
    const getColorIcon = (colorValue) => {
        const option = options.find(option => option.value == colorValue);
        return option ? option.label : null;
    };

    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return `　${date.getMonth() + 1}月${date.getDate()}日`;
    };

    const shoppingItemsHeader = (
        <thead>
            <tr>
                <th colspan="4" scope="col" class="px-2 py-2 text-center text-lg font-medium text-gray-500 uppercase dark:text-neutral-500">
                    買い物予定日：{formatDate(ShoppingListInfo.next_shopping_day)}</th>
            </tr>
        </thead>
    )

    const shoppingItemsData = shoppingItems.map((item, index) => (
        <>
        <tbody class="divide-y divide-gray-200 dark:divide-neutral-70">

            <tr key={index}>
                <td class="px-1 py-1 whitespace-nowrap text-sm font-medium text-gray-800 dark:text-neutral-200">
                    {getColorIcon(item.color)}
                </td>
                <td class="px-2 py-2 whitespace-nowrap text-start text-sm w-32 font-medium text-gray-800 dark:text-neutral-200">
                    {item.item_name}
                </td>
                <td class="px-2 py-2 whitespace-nowrap text-sm w-20 font-medium text-gray-800 dark:text-neutral-200">
                    <BoughtOrPassBtn
                        onClick={ () => handleBought(item) }
                        children="買った"
                        disabled={!item.to_list}
                        />
                </td>
                <td class="px-2 py-2 whitespace-nowrap text-sm w-20 font-medium text-gray-800 dark:text-neutral-200">
                    <BoughtOrPassBtn
                        onClick={ () => handlePass(item) }
                        children="見送る"
                        disabled={!item.to_list}
                        />
                </td>
            </tr>
        </tbody>

        </>
                )
    );

    const shoppingListFieldPanel = (
        <div class="flex flex-col w-full">
            <div class="-m-1.5 overflow-x-auto overflow-y-auto  mx-auto max-w-128">
                <div class="p-1.5 min-w-full inline-block align-middle">
                    <div class="overflow-hidden border rounded-lg">
                        <table class="text-center min-w-full divide-y divide-gray-200 dark:divide-neutral-700">
                            { shoppingItemsHeader }

                            {shoppingItemsData}
                        </table>
                    </div>
                </div>
            </div>
        </div>
    );

    return(
        <>
            <div className='flex justify-center flex-col'>
                { shoppingListFieldPanel }
            </div>
        </>
    )
}


//管理商品画面のパネル
function ItemsListPanel() {
    const [itemsState, setItemsState] = useState([]);
    const [listsInfo, setListsInfo] = useState([]);
    const dispatch = useDispatch();
    const selectedList = useSelector(state => state.selectedList);
    const userSetRemind = useSelector(state => state.user.remind);
    const token = useSelector(state => state.token.token);
    const [errorMessage, setErrorMessage] = useState("");


    // const items = useSelector(state => state.items.items);

    const handleAddNewItem = async() => {
        try {
            const newItemResponse = await addNewItemRequest(selectedList.list_id, token);
            const itemsResponse = await fetchItemsOfListRequest(selectedList.list_id, token);
            setItemsState(itemsResponse.data.items);
        } catch (err) {
            console.error('Failed to add new item:', err);
        }
    };
    //読み込み時にitemデータを取得
    useEffect(() => {
        setErrorMessage("");
        const fetchListAndItemsInfo = async() => {
            if(selectedList.is_owner){
                const itemsInfo = await fetchItemsOfListRequest(selectedList.list_id, token);
                setItemsState(itemsInfo.data.items);
                // const listsInfo = await fetchListInfoRequest(selectedList.list_id, token);
                // dispatch(setSelectedList(listsInfo.data));
                // setListsInfo(listsInfo.data);
            } else {
                if(selectedList.authority){
                    const itemsInfo = await fetchItemsOfListRequest(selectedList.list_id, token);
                    setItemsState(itemsInfo.data.items);
                }else{
                    //clear
                    setItemsState([]);
                    setErrorMessage("※お買い物リストの閲覧のみ可能です。")
                }
            }
        };
        fetchListAndItemsInfo();
    }, [selectedList]);

    //テキスト形式の項目の更新
    const updateItem = async(item, key, newValue) => {
        const response = await updateItemInfoRequest(selectedList.list_id, item.item_id, key, newValue, token);
        setItemsState(prevItems => prevItems.map(prevItem =>
            prevItem.item_id === item.item_id ? { ...prevItem, [key]: newValue } : prevItem
        ));
    };

    //管理対象を切り替える
    const changeManageTarget = async(item) => {
        const newManageTarget = !item.manage_target;
        try {
            await updateItemInfoRequest(selectedList.list_id, item.item_id, "manage_target", newManageTarget, token);
            setItemsState(prevItems => prevItems.map(prevItem => 
                prevItem.item_id === item.item_id ? { ...prevItem, manage_target: newManageTarget } : prevItem
            ));
        } catch (err) {
            console.error('Failed to update manage target:', err);
        }
    }
    //itemごとの通知について切り替える
    const changeRemindByItem = async(item) => {
        const newRemindByItem = !item.remind_by_item;
        try {
            await updateItemInfoRequest(selectedList.list_id, item.item_id, "remind_by_item", newRemindByItem, token);
            setItemsState(prevItems => prevItems.map(prevItem => 
                prevItem.item_id === item.item_id ? { ...prevItem, remind_by_item: newRemindByItem } : prevItem
            ));
        } catch (err) {
            console.error('Failed to update manage target:', err);
        }
    }
    //買い物リストに入れる
    const toShoppingLists = async(item) => {
        try {
            await updateItemInfoRequest(selectedList.list_id, item.item_id, "to_list", true, token);
            setItemsState(prevItems => prevItems.map(prevItem => 
                prevItem.item_id === item.item_id ? { ...prevItem, to_list: true } : prevItem
            ));
        } catch (err) {
            console.error('Failed to update manage target:', err);
        }
    }
    
    const deleteItemtest = async(item) => {
        try {
            const response = await deleteItemRequest(selectedList.list_id, item.item_id, token);
            if (response.status === 200) {
                setItemsState(prevItems => prevItems.filter(prevItem => prevItem.item_id !== item.item_id));
            } else {
                console.error('Failed to delete item:', response);
            }
        } catch(err) {
            console.error('Failed to delete item:', err);
        }
    }

    const itemsData = itemsState.map((item) => (
        <>
            
            <tbody class="divide-y divide-gray-200 dark:divide-neutral-700">
                <tr key={item.item_id}>
                    {/*管理対象*/}
                    <td class="px-2 py-2 whitespace-nowrap text-center text-sm font-medium text-gray-800 dark:text-neutral-200">
                        <input
                            type="checkbox"
                            checked={item.manage_target}
                            onChange={() => changeManageTarget(item)}
                            className='w-8'
                              />
                    </td>
                    {/*カテゴリカラー*/}
                    <td class="px-1 py-1 whitespace-nowrap text-sm font-medium text-gray-800 dark:text-neutral-200">
                        <SimpleSelectBox
                            color={item.color}
                            onChange={(selectedOption) => updateItem(item, 'color', selectedOption.value)}
                        />
                    </td>
                    {/*商品名*/}
                    <td class="px-2 py-2 whitespace-nowrap text-sm w-32 font-medium text-gray-800 dark:text-neutral-200">
                        <EditableInput
                            className=' '
                            initialValue={item.item_name}
                            onSave={newValue => updateItem(item, 'item_name', newValue)}
                            />
                    </td>
                    {/*消費サイクル*/}
                    <td class="px-2 py-2 whitespace-nowrap text-center text-sm w-32 font-medium text-gray-800 dark:text-neutral-200">
                        <EditableInput
                            className='text-center w-14'
                            initialValue={item.consume_cycle}
                            onSave={newValue => updateItem(item, 'consume_cycle', newValue)}
                            />日
                    </td>
                    {/*直近の開封日*/}
                    <td class="px-2 py-2 whitespace-nowrap text-sm font-medium text-gray-800 dark:text-neutral-200">
                        <EditableDateInput
                        initialValue={item.last_open_at}
                        onSave={newValue => updateItem(item, 'last_open_at', newValue)}
                        />
                    </td>
                    {/*リンク*/}
                    <td class="px-2 py-2 whitespace-nowrap text-sm text-start font-medium text-gray-800 dark:text-neutral-200">
                        <EditableInput
                            className='w-16 text-center'
                            initialValue={item.item_url}
                            onSave={newValue => updateItem(item, 'item_url', newValue)}
                            />
                    </td>
                    {/*最終購入日*/}
                    <td class="px-2 py-2 whitespace-nowrap text-sm font-medium text-gray-800 dark:text-neutral-200">
                        <EditableDateInput
                            initialValue={item.last_purchase_at}
                            onSave={newValue => updateItem(item, 'last_purchase_at', newValue)}
                            />
                    </td>
                    {/*リスト追加ボタン*/}
                    <td class="px-2 py-2 whitespace-nowrap text-sm w-20 font-medium text-gray-800 dark:text-neutral-200">
                        <ToShoppingListBtn
                            onClick={ () => toShoppingLists(item) }
                            children="追加"
                            disabled={item.to_list || !item.manage_target}
                        />
                    </td>
                    {/*通知対象*/}
                    <td class="px-2 py-2 whitespace-nowrap text-center text-sm font-medium text-gray-800 dark:text-neutral-200">
                        <input
                            type='checkbox'
                            checked={item.remind_by_item}
                            onChange={ () => changeRemindByItem(item) }
                            disabled={!userSetRemind}
                            className='w-8'
                            />
                    </td >
                    {/* 削除 */}
                    <td class='px-2 py-2'>
                        <TrashBtn onClick={ () => deleteItemtest(item)} />
                    </td>
                </tr>
            </tbody>

        </>
        )
    );



    const itemsListFieldPanel = (
        <div class="flex flex-col">
                <div class="-m-1.5 overflow-x-auto border">
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
                            {/* { itemsHeader } */}
                            { itemsData }
                        </table>
                    </div>
                </div>
            </div>
        </div>
    );
    
    
    
    
    return (
        <>
        <div className='flex justify-center flex-col'>

            { itemsListFieldPanel }
            <div className='flex justify-center mt-2 '>
                <button type='button' className='' onClick={handleAddNewItem}>
                    +商品を追加する
                </button>


            </div>
            <div className='flex justify-center text-red-500'>
                {errorMessage}
            </div>
        </div>



        </>
    )
}


export { ShoppingListPanel, ItemsListPanel, EditableInput };