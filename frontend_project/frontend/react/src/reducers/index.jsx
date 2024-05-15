import { combineReducers } from "redux";
import userReducer from './userSlice';
import itemsReducer from './itemSlice';
import selectedListReducer from './selectedListSlice';
import shoppingItemsReducer from './shoppingItemsSlice';
import { RESET_APP_STATE } from './actionTypes';

const appReducer = combineReducers({
    user: userReducer,
    items: itemsReducer,
    selectedList: selectedListReducer,
    shoppingItems: shoppingItemsReducer,
});

const rootReducer = (state, action) => {
    //初期化
    if (action.type === RESET_APP_STATE) {
        state = undefined;
    }
    return appReducer(state, action);
};

export default rootReducer;