import { setSelectedList } from "../reducers/selectedListSlice";
import { setUser } from "../reducers/userSlice";
import { addNewListRequest, fetchUserInfoRequest } from "./Requests"
import { useDispatch, useSelector } from "react-redux";

const AddNewList = () => {
    const dispatch = useDispatch();
    const token = useSelector(state => state.token.token);


    return async() => {
        await addNewListRequest(token);
        const response = await fetchUserInfoRequest(token);
        // dispatch(setUser(response.data.user));
        // dispatch(setUser({lists:response.data.lists}));
        dispatch(setSelectedList(response.data.lists[response.data.lists.length -1]));
    };
};

export default AddNewList;