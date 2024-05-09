import { createSlice } from '@reduxjs/toolkit';

export const userSlice = createSlice({
    name: 'user',
    initialState: {
		default_list: null,
		email: null,
		have_list: null,
		invitation: null,
		line_id: null,
		line_status: null,
		remind: null,
		remind_time: null,
		remind_timing: null,
		request :null,
		user_icon: null,
        user_id: null,
        user_name: null,
    },
    reducers: {
        setUser: (state, action) => {
            return { ...state, ...action.payload };
            // state.default_list = action.payload.default_list,
            // state.email = action.payload.email,
            // state.have_list = action.payload.have_list,
            // state.invitation = action.payload.invitation,
            // state.line_id = action.payload.line_id,
            // state.line_status = action.payload.line_status,
            // state.remind = action.payload.remind,
            // state.remind_time = action.payload.remind_time,
            // state.remind_timing = action.payload.remind_timing,
            // state.request = action.payload.request,
            // state.user_icon = action.payload.user_icon,
            // state.user_id = action.payload.user_id,
            // state.user_name = action.payload.user_name;
        },
        clearUser: (state) => {
            state.user_id = null;
            state.user_name = null;
        }
    },
});

export const { setUser, clearUser } = userSlice.actions;

export default userSlice.reducer;