import { setItemAllInfo } from "../reducers/itemSlice";
import { setUser } from "../reducers/userSlice";
import { addNewItemRequest, addNewListRequest, fetchItemsOfListRequest, fetchUserInfoRequest } from "./Requests"
import { useDispatch } from "react-redux";

const AddNewItem = (selectedListList_id) => {
    const dispatch = useDispatch();

    return async() => {
        await addNewItemRequest(selectedListList_id);
        const response = await fetchItemsOfListRequest(selectedListList_id);
        console.log(response);
        dispatch(setItemAllInfo(response.data.items));

    };
};

export default AddNewItem;