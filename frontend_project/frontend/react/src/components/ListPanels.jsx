import React, { useEffect, useRef, useState }  from 'react';
import '../styles/Lists.css'
import { AddBtn, BoughtOrPassBtn, ShoppingBtn, ToShoppingListBtn } from './Buttons';
import { useDispatch, useSelector } from 'react-redux';
import { deleteItemRequest, fetchItemsOfListRequest, fetchShoppingListRequest, updateItemInfoRequest } from '../utils/Requests';
import { setItemAllInfo, updateColor, updateConsumeCycle, updateItemName, updateItemUrl, updateLastOpenAt, updateLastPurchaseAt, updateManageTarget, updateRemindByItem, updateToList, deleteItem } from '../reducers/itemSlice';
import "../styles/CategoryColor.css";
import EditableDateInput from './EditableDateInput';
import AddNewItem from '../utils/AddNewItem';
import { setShoppingItemsAllInfo } from '../reducers/shoppingItemsSlice';

function ListFieldTitle({ title }) {
    return(
        <>
            <div className='list-field-title'>
                { title }
            </div>
        </>
    );
}

//買い物リスト画面のパネル
function ShoppingListPanel() {
    const selectedList = useSelector(state => state.selectedList);
    const shoppingItems = useSelector(state => state.shoppingItems)
    // const list_title = useSelector((state) => state.);
    const items = useSelector(state => state.shoppingItems.items);
    const dispatch = useDispatch();
    //読み込み時にshoppingItemデータを取得
    useEffect(() => {
        const fetchShoppingList = async() => {
            const response = await fetchShoppingListRequest(selectedList.list_id);
            console.log('data;',response.data);
            dispatch(setShoppingItemsAllInfo(response.data));
            console.log(shoppingItems);
        }
        fetchShoppingList();
    },[]);

    //見送りボタン（買い物リストから外す）
    const handlePass = async(item) => {
        try {
            const response = await updateItemInfoRequest(selectedList.list_id, item.item_id, "to_list", false);
            // dispatch(updateToList({ item_id: item.item_id, to_list: response.data.to_list }));
            const currentShoppingList = await fetchShoppingListRequest(selectedList.list_id);
            console.log(currentShoppingList.data);
            dispatch(setShoppingItemsAllInfo(currentShoppingList.data));
        }catch (err){
            console.error('Failed to update manage target:', err);
        }
    }
    //買ったボタン（買い物リストから外す・購入日を今日にする）
    const handleBought = async(item) => {
        try{
            const response = await updateItemInfoRequest(selectedList.list_id, item.item_id, "to_list", false);
            
            const today = new Date();
            const formattedDate = today.toISOString().slice(0, 10);
            const response2 = await updateItemInfoRequest(selectedList.list_id, item.item_id, "last_purchase_at", formattedDate);
            const currentShoppingList = await fetchShoppingListRequest(selectedList.list_id);
            dispatch(setShoppingItemsAllInfo(currentShoppingList.data));
            
            const response3 = await fetchItemsOfListRequest(selectedList.list_id);
            console.log("response3:",response3);
            dispatch(setItemAllInfo(response3.data.items));

        }catch (err){
            console.error('Failed to update manage target:', err);
        }
    }

    const shoppingItemsHeader = (
        <thead>
            <tr className='text-center'>
                <th colSpan="4">次の買い物予定日：{shoppingItems.items.next_shopping_day}</th>
            </tr>
        </thead>
    )

    const shoppingItemsData = shoppingItems.items.items.map((item, index) => (

        <tr className="text-center border-b" key={index}>
            <td>
                {item.color}
            </td>
            <td>
                {item.item_name}
            </td>
            <td>
                <BoughtOrPassBtn
                    onClick={ () => handleBought(item) }
                    children="買った"
                    disabled={!item.to_list}
                    />
            </td>
            <td>
                <BoughtOrPassBtn
                    onClick={ () => handlePass(item) }
                    children="見送る"
                    disabled={!item.to_list}
                    />
            </td>
        </tr>
                )
    );

    const shoppingListFieldPanel = (
        <div className='list-field'>
            <table className='table-fixed w-full'>
                { shoppingItemsHeader }
                <tbody>
                    {shoppingItemsData}
                </tbody>
            </table>

        </div>
    );

    return(
        <>
            <div className='list-field-container'>
                <ListFieldTitle title={selectedList.list_name} />
                { shoppingListFieldPanel }
            </div>
        </>
    )
}

//inputフォームの共通化
function EditableInput({ initialValue, onSave, onComposition }) {
    const [value, setValue] = useState(initialValue);
    const inputRef = useRef(null);
    const [isComposing, setIsComposing] = useState(false);

    const handleBlur = () => {
        if (!isComposing) {
            onSave(value);
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === "Enter" && !isComposing) {
            e.preventDefault();
            inputRef.current.blur();
        }
    };

    return (
        <input
            className='w-full text-center'
            ref={inputRef}
            type="text"
            value={value}
            onChange={e => setValue(e.target.value)}
            onBlur={handleBlur}
            onKeyDown={handleKeyDown}
            onCompositionStart={() => setIsComposing(true)}
            onCompositionEnd={() => {
                setIsComposing(false);
                onSave(value);
            }}
        />
    );
}


//管理商品画面のパネル
function ItemsListPanel() {
    const [itemListItems, setItemListItems] = useState([]);
    const dispatch = useDispatch();
    const selectedList = useSelector(state => state.selectedList);
    const items = useSelector(state => state.items.items);
    const handleAddNewItem = AddNewItem(selectedList.list_id);

    //読み込み時にitemデータを取得
    useEffect(() => {
        const fetchItemsOfList = async() => {
            const response = await fetchItemsOfListRequest(selectedList.list_id);
            setItemListItems(response.data.items);
            console.log(itemListItems);
            console.log('update',itemListItems);
            dispatch(setItemAllInfo(response.data.items));
        };
        fetchItemsOfList();
    }, []);

    //テキスト形式の項目の更新
    const updateItem = async(item, key, newValue) => {
        if (key === 'item_name') {
            const response = await updateItemInfoRequest(selectedList.list_id, item.item_id, 'item_name', newValue);
            dispatch(updateItemName({ item_id: item.item_id, item_name: response.data.item_name }));
        }
        if (key === "color") {
            const response = await updateItemInfoRequest(selectedList.list_id, item.item_id, 'color', newValue);
            dispatch(updateColor({ item_id: item.item_id, color: response.data.color }));
        }
        if (key === "consume_cycle") {
            const response = await updateItemInfoRequest(selectedList.list_id, item.item_id, 'consume_cycle', newValue);
            dispatch(updateConsumeCycle({ item_id: item.item_id, consume_cycle: response.data.consume_cycle }));
        }
        if (key === "last_purchase_at") {
            const response = await updateItemInfoRequest(selectedList.list_id, item.item_id, 'last_purchase_at', newValue);
            dispatch(updateLastPurchaseAt({ item_id: item.item_id, last_purchase_at: response.data.last_purchase_at }));
        }
        if (key === "last_open_at") {
            const response = await updateItemInfoRequest(selectedList.list_id, item.item_id, 'last_open_at', newValue);
            dispatch(updateLastOpenAt({ item_id: item.item_id, last_open_at: response.data.last_open_at }));
        }
        if (key === "item_url") {
            const response = await updateItemInfoRequest(selectedList.list_id, item.item_id, 'item_url', newValue);
            dispatch(updateItemUrl({ item_id: item.item_id, item_url: response.data.item_url }));
        }
        // if (key === "to_list") {
        //     const response = await updateItemInfoRequest(selectedList.list_id, item.item_id, 'to_list', newValue);
        //     dispatch(updateToList({ item_id: item.item_id, to_list: response.data.to_list }));
        // }
    };
    //管理対象を切り替える
    const changeManageTarget = async(item) => {
        const newManageTarget = !item.manage_target;
        try {
            const response = await updateItemInfoRequest(selectedList.list_id, item.item_id, "manage_target", newManageTarget);
            dispatch(updateManageTarget({ item_id: item.item_id, manage_target: response.data.manage_target }));
        }catch (err){
            console.error('Failed to update manage target:', err)
        }
    }
    //itemごとの通知について切り替える
    const changeRemindByItem = async(item) => {
        const newRemindByItem = !item.remind_by_item;
        try {
            const response = await updateItemInfoRequest(selectedList.list_id, item.item_id, "remind_by_item", newRemindByItem);
            dispatch(updateRemindByItem({ item_id: item.item_id, remind_by_item: response.data.remind_by_item }));
        }catch (err){
            console.error('Failed to update manage target:', err);
        }
    }
    //買い物リストに入れる
    const toShoppingLists = async(item) => {
        try {
            const response = await updateItemInfoRequest(selectedList.list_id, item.item_id, "to_list", true);
            dispatch(updateToList({ item_id: item.item_id, to_list: response.data.to_list }));
        }catch (err){
            console.error('Failed to update manage target:', err);
        }
    }
    //item削除
    const deleteItemtest = async(item) => {
    //     const response = await deleteItemRequest(selectedList.list_id, item.item_id);
    //     // dispatch(deleteItem(item.item_id));
    //     // const updateItems = itemListItems.filter(listItem => listItem.item_id !== item.item_id);
    //     setItemListItems(itemListItems.filter((listItem,i) => i !== index));
    //     console.log(item.item_id);
    //     console.log(itemListItems);
    // };
    //     try {
    //         const response = await deleteItemRequest(selectedList.list_id, item.item_id);
    //         dispatch(deleteItem(item.item_id))
    //         const response1 = await fetchItemsOfListRequest(selectedList.list_id);
    //         dispatch(setItemAllInfo(response1.data.items));
    //     }catch(err){
    //         console.error('Failed to update manage target:', err);
    //     }
    // }
        try {
            const response = await deleteItemRequest(selectedList.list_id, item.item_id);
            if (response.status === 200) {
                dispatch(deleteItem(item.item_id));
                const response1 = await fetchItemsOfListRequest(selectedList.list_id);
                if (response1.status === 200) {
                    dispatch(setItemAllInfo(response1.data.items));
                } else {
                    console.error('Failed to refetch items:', response1);
                }
            } else {
                console.error('Failed to delete item:', response);
            }
        } catch(err) {
            console.error('Failed to delete item:', err);
        }
    }


    //     try {
    //             const response = await deleteItemRequest(selectedList.list_id, item.item_id);
    //             dispatch(clearItem(item.item_id))
    //         }catch(err){
    //             console.error('Failed to update manage target:', err);
    //         }
    //     }
    //         const response = await deleteItemRequest(selectedList.list_id, item.item_id);
    //         if (response.status === 200) {
    //             dispatch(deleteItem(item.item_id));
    //             console.log('Item deleted successfully');
    //         } else {
    //             console.error('Failed to delete item');
    //         }
    //     } catch (error) {
    //         console.error('Error deleting item:', error);
    //     }
    // };
    // const test = () => {
    //     console.log(itemListItems);
    // }

    //カテゴリカラーのselect
    const CategoryColorSelector = ({ color, onChange }) => {
        return(
            <>
                <select value={ color } onChange={ onChange } className='category-color-selector'>
                    <option value="0" >赤</option>
                    <option value="1" >ピンク</option>
                    <option value="2" >オレンジ</option>
                    <option value="3" >黄</option>
                    <option value="4" >黄緑</option>
                    <option value="5" >緑</option>
                    <option value="6" >水色</option>
                    <option value="7" >青</option>
                    <option value="8" >薄紫</option>
                    <option value="9" >紫</option>
                    <option value="10" >グレー</option>
                </select>
            </>
        );
    };

    const itemsHeader = (
        <thead>
            <tr className="text-center">
                <th>管理する</th>
                <th colSpan="2">商品名</th>
                <th>消費サイクル</th>
                <th>直近の開封日</th>
                <th>サイトのリンク</th>
                <th>最終購入日</th>
                <th>   </th>
                <th>通知する</th>
            </tr>
        </thead>
    );

    const itemsData = items.map((item) => (
        <>
        <tr className="text-center border-b" key={item.item_id}>
            {/*管理対象*/}
            <td>
                <input
                    type="checkbox"
                    checked={item.manage_target}
                    onChange={() => changeManageTarget(item)}  />
            </td>
            {/*カテゴリカラー*/}
            <td>
                <CategoryColorSelector
                    color={item.color}
                    onChange={(e) => updateItem(item, 'color', e.target.value)}
                />
            </td>
            {/*商品名*/}
            <td>
                <EditableInput
                    initialValue={item.item_name}
                    onSave={newValue => updateItem(item, 'item_name', newValue)}
                    />
            </td>
            {/*消費サイクル*/}
            <td>
                <EditableInput
                    initialValue={item.consume_cycle}
                    onSave={newValue => updateItem(item, 'consume_cycle', newValue)}
                    />
            </td>
            {/*直近の開封日*/}
            <td>
                <EditableDateInput
                initialValue={item.last_open_at}
                onSave={newValue => updateItem(item, 'last_open_at', newValue)}
                    />
            </td>
            {/*リンク*/}
            <td>
                <EditableInput
                    initialValue={item.item_url}
                    onSave={newValue => updateItem(item, 'item_url', newValue)}
                    />
            </td>
            {/*最終購入日*/}
            <td>
                <EditableDateInput
                    initialValue={item.last_purchase_at}
                    onSave={newValue => updateItem(item, 'last_purchase_at', newValue)}
                    />
            </td>
            {/*リスト追加ボタン*/}
            <td>
                <ToShoppingListBtn
                    onClick={ () => toShoppingLists(item) }
                    children="追加する"
                    disabled={item.to_list}
                />
            </td>
            {/*通知対象*/}
            <td>
                <input
                    type='checkbox'
                    checked={item.remind_by_item}
                    onChange={ () => changeRemindByItem(item) } />
            </td>
            {/* 削除 */}
            <td>
                <button onClick={ () => deleteItemtest(item)}>削除</button>
            </td>
        </tr>
            
        </>
        )
    );



    const itemsListFieldPanel = (
        <div className='list-field'>
            <table className="table-fixed w-full">
                { itemsHeader }
                <tbody>
                    { itemsData }

                </tbody>
            </table>
            <AddBtn children="+" onClick={handleAddNewItem} />
        </div>
    );

    


    return (
        <>
            <div className='item-field-container'>
                <ListFieldTitle title={selectedList.list_name} />
                { itemsListFieldPanel }
                

            </div>
        </>
    )
}


export { ShoppingListPanel, ItemsListPanel };