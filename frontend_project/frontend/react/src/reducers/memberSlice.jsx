import { createSlice } from '@reduxjs/toolkit';

export const memberSlice = createSlice({
    name: 'member',
    initialState: {
        member:[]
    },
    reducers: {
        setMember: (state, action) => {
            state.member = action.payload;
        }
    }
});

export const
    { setMember } = memberSlice.actions;
export default memberSlice.reducer;