import React, { useEffect, useRef, useState }  from 'react';
import '../styles/Lists.css'
import { ShoppingBtn } from './Buttons';
import { useDispatch, useSelector } from 'react-redux';
import { fetchItemsOfListRequest, updateItemInfoRequest } from '../utils/Requests';
import { setItemAllInfo, updateColor, updateConsumeCycle, updateItemName, updateItemUrl, updateLastOpenAt, updateLastPurchaseAt, updateManageTarget, updateRemindByItem, updateToList } from '../reducers/itemSlice';

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
    const list_title = useSelector((state) => state.user.lists[0].list_name);
    const shoppingItems = (
        <div className='flex justify-center text-center items-center border-b'>
            <img className='flex-none ' alt='ctg' />
            <div className='flex-none' >商品名</div>
            <div className='flex-none'>
                <ShoppingBtn children="買った"/>
            </div>
            <div className='flex-none'>
                <ShoppingBtn children="見送り"/>
            </div>
        </div>
    );

    const shoppingListFieldPanel = (
        <div className='list-field'>
            <p className='text-center'>日付</p>
            { shoppingItems }
        </div>
    );

    return(
        <>
            <div className='list-field-container'>
                <ListFieldTitle title={list_title} />
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
    const dispatch = useDispatch();
    const selectedList = useSelector(state => state.selectedList);
    const items = useSelector(state => state.item.items);

    //読み込み時にitemデータを取得
    useEffect(() => {
        const fetchItemsOfList = async() => {
            const response = await fetchItemsOfListRequest(selectedList.list_id);
            dispatch(setItemAllInfo(response.data.items))
        };
        fetchItemsOfList();
    }, []);

    //テキスト形式の項目の更新
    const updateItem = async(item, key, newValue) => {
        if (key === 'item_name') {
            const response = await updateItemInfoRequest(selectedList.list_id, item.item_id, 'item_name', newValue);
            dispatch(updateItemName({ item_id: item.item_id, item_name: response.data.item_name }));
        }
        // if (key === "color") {
        //     const response = await updateItemInfoRequest(selectedList.list_id, item.item_id, 'color', newValue);
        //     dispatch(updateColor({ item_id: item.item_id, color: response.data.color }));
        // }
        if (key === "consume_cycle") {
            const response = await updateItemInfoRequest(selectedList.list_id, item.item_id, 'consume_cycle', newValue);
            dispatch(updateConsumeCycle({ item_id: item.item_id, consume_cycle: response.data.consume_cycle }));
        }
        // if (key === "last_purchase_at") {
        //     const response = await updateItemInfoRequest(selectedList.list_id, item.item_id, 'last_purchase_at', newValue);
        //     dispatch(updateLastPurchaseAt({ item_id: item.item_id, last_purchase_at: response.data.last_purchase_at }));
        // }
        // if (key === "last_open_at") {
        //     const response = await updateItemInfoRequest(selectedList.list_id, item.item_id, 'last_open_at', newValue);
        //     dispatch(updateLastOpenAt({ item_id: item.item_id, last_open_at: response.data.last_open_at }));
        // }
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

    const itemsData = items.map((item, index) => (
        <tr className="text-center" key={index}>
            {/*管理対象*/}
            <td>
                <input
                    type="checkbox"
                    checked={item.manage_target}
                    onChange={() => changeManageTarget(item)}  />
            </td>
            {/*カテゴリカラー*/}
            <td>{item.color}</td>
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
                <EditableInput
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
                <EditableInput
                    initialValue={item.last_purchase_at}
                    onSave={newValue => updateItem(item, 'last_purchase_at', newValue)}
                    />
            </td>
            {/*リスト追加ボタン*/}
            <td>ボタンto_listfalse</td>
            {/*通知対象*/}
            <td>
                <input
                    type='checkbox'
                    checked={item.remind_by_item}
                    onChange={() => changeRemindByItem(item) } />
            </td>
        </tr>
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