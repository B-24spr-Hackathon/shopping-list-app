import { createSlice } from '@reduxjs/toolkit';

export const itemSlice = createSlice({
    name: 'items',
    initialState: {
        items:[]
    },
    reducers: {
        setItemAllInfo: (state, action) => {
            state.items = action.payload;
        },
        updateManageTarget: (state, action) => {
            const { item_id, manage_target } = action.payload;
            const index = state.items.findIndex(item => item.item_id === item_id);
            if (index !== -1) {
                state.items[index].manage_target = manage_target;
            }
        },
        updateRemindByItem: (state, action) => {
            const { item_id, remind_by_item } = action.payload;
            const index = state.items.findIndex(item => item.item_id === item_id);
            if (index !== -1) {
                state.items[index].remind_by_item = remind_by_item;
            }
        },
        updateItemName: (state, action) => {
            const { item_id, item_name } = action.payload;
            const index = state.items.findIndex(item => item.item_id === item_id);
            if (index !== -1) {
                state.items[index].item_name = item_name;
            }
        },
        updateColor: (state, action) => {
            const { item_id, color } = action.payload;
            const index = state.items.findIndex(item => item.item_id === item_id);
            if (index !== -1) {
                state.items[index].color = color;
            }
        },
        updateConsumeCycle: (state, action) => {
            const { item_id, consume_cycle } = action.payload;
            const index = state.items.findIndex(item => item.item_id === item_id);
            if (index !== -1) {
                state.items[index].consume_cycle = consume_cycle;
            }
        },
        updateLastPurchaseAt: (state, action) => {
            const { item_id, last_purchase_at } = action.payload;
            const index = state.items.findIndex(item => item.item_id === item_id);
            if (index !== -1) {
                state.items[index].last_purchase_at = last_purchase_at;
            }
        },
        updateLastOpenAt: (state, action) => {
            const { item_id, last_open_at } = action.payload;
            const index = state.items.findIndex(item => item.item_id === item_id);
            if (index !== -1) {
                state.items[index].last_open_at = last_open_at;
            }
        },
        updateItemUrl: (state, action) => {
            const { item_id, item_url } = action.payload;
            const index = state.items.findIndex(item => item.item_id === item_id);
            if (index !== -1) {
                state.items[index].item_url = item_url;
            }
        },
        updateToList: (state, action) => {
            const { item_id, to_list } = action.payload;
            const index = state.items.findIndex(item => item.item_id === item_id);
            if (index !== -1) {
                state.items[index].to_list = to_list;
            }
        },
        deleteItem: (state, action) => {
            // const item_id = action.payload;  // アクションから item_id を受け取る
            // state.items = state.items.filter(item => item.item_id !== item_id);

            const itemId = action.payload;  // アクションから item_id を受け取る
            const index = state.items.findIndex(item => item.item_id === itemId);
            if (index !== -1) {
                state.items.splice(index, 1);  // 配列から該当するアイテムを削除
            }
}
        
    }
});

export const
    {
        setItemAllInfo,
        deleteItem,
        updateManageTarget,
        updateRemindByItem,
        updateItemName,
        updateColor,
        updateConsumeCycle,
        updateLastPurchaseAt,
        updateLastOpenAt,
        updateItemUrl,
        updateToList,
    } = itemSlice.actions;
export default itemSlice.reducer;