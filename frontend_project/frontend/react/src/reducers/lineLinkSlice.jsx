import { createSlice } from '@reduxjs/toolkit';

export const lineLinkSlice = createSlice({
    name: 'lineLink',
    initialState: {
		otp: null,
        url: null,
    },
    reducers: {
        setLineLink: (state, action) => {
            return { ...state, ...action.payload };
            
        },
        clearLineLink: (state) => {
            state.otp = null;
            state.url = null;
        }
    },
});

export const { setLineLink, clearLineLink } = lineLinkSlice.actions;
export default lineLinkSlice.reducer;