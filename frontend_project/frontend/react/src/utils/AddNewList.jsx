import { setUser } from "../reducers/userSlice";
import { addNewListRequest, fetchUserInfoRequest } from "./Requests"
import { useDispatch } from "react-redux";

const AddNewList = () => {
    const dispatch = useDispatch();

    return async() => {
        await addNewListRequest();
        const response = await fetchUserInfoRequest();
        console.log(response);
        dispatch(setUser(response.data.user));
        dispatch(setUser({lists:response.data.lists}));
    };
};

export default AddNewList;