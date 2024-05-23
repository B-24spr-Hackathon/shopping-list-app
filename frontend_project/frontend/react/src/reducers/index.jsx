import { combineReducers } from "redux";
import userReducer from './userSlice';
import itemsReducer from './itemSlice';
import selectedListReducer from './selectedListSlice';
import shoppingItemsReducer from './shoppingItemsSlice';
import tokenReducer from './tokenSlice';
import lineLinkReducer from './lineLinkSlice';
import memberReducer from "./memberSlice";
import { RESET_APP_STATE } from './actionTypes';

const appReducer = combineReducers({
    user: userReducer,
    items: itemsReducer,
    selectedList: selectedListReducer,
    shoppingItems: shoppingItemsReducer,
    token: tokenReducer,
    lineLink: lineLinkReducer,
    member: memberReducer,

});

const rootReducer = (state, action) => {
    //初期化
    if (action.type === RESET_APP_STATE) {
        const { selectedList } = state; // 現在のselectedListの状態を取得
        state = undefined;
        state = appReducer(state, action); // 他の部分を初期化
        // state.selectedList = selectedList; // selectedListの状態を復元
    }
    return appReducer(state, action);
};

export default rootReducer;