import { setSelectedList } from "../reducers/selectedListSlice";
import { setUser } from "../reducers/userSlice";
import { addNewListRequest, fetchUserInfoRequest } from "./Requests"
import { useDispatch } from "react-redux";

const AddNewList = () => {
    const dispatch = useDispatch();

    return async() => {
        await addNewListRequest();
        const response = await fetchUserInfoRequest();
        dispatch(setUser(response.data.user));
        dispatch(setUser({lists:response.data.lists}));
        dispatch(setSelectedList(response.data.lists[response.data.lists.length -1]));
    };
};

export default AddNewList;