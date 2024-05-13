import { createSlice } from '@reduxjs/toolkit';

export const selectedListSlice = createSlice({
    name: 'selectedList',
    initialState: {
        list_id: null,
        list_name: null,
    },
    reducers: {
        setSelectedList: (state, action) => {
            return { ...state, ...action.payload };
        },
        clearSelectedList: (state) => {
            
            
        }
    },
});

export const { setSelectedList, clearSelectedList } = selectedListSlice.actions;
export default selectedListSlice.reducer;