import { combineReducers } from "redux";
import userReducer from './userSlice';
import itemReducer from './itemSlice';
import selectedListReducer from './selectedListSlice'

const rootReducer = combineReducers({
    user: userReducer,
    item: itemReducer,
    selectedList: selectedListReducer,
});

export default rootReducer;