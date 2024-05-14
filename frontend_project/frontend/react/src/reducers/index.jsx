import { combineReducers } from "redux";
import userReducer from './userSlice';
import itemReducer from './itemSlice';
import selectedListReducer from './selectedListSlice'
import { RESET_APP_STATE } from './actionTypes';

const appReducer = combineReducers({
    user: userReducer,
    items: itemReducer,
    selectedList: selectedListReducer,
});

const rootReducer = (state, action) => {
    //初期化
    if (action.type === RESET_APP_STATE) {
        state = undefined;  
    }
    return appReducer(state, action);
};

export default rootReducer;