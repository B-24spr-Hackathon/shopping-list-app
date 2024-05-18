import { createSlice } from '@reduxjs/toolkit';

export const selectedListSlice = createSlice({
    name: 'selectedList',
    initialState: {
        list_id: null,
        list_name: null,
        shopping_day: null,
        guests_info: [],
    },
    reducers: {
        setSelectedList: (state, action) => {
            return { ...state, ...action.payload };
        },
        // setSelectedList: (state, action) => {
        //     state.selectedList = action.payload;
        // },
        clearSelectedList: (state) => {
            
            
        }
    },
});

export const { setSelectedList, clearSelectedList } = selectedListSlice.actions;
export default selectedListSlice.reducer;