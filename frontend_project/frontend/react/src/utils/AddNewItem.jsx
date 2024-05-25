import { setItemAllInfo } from "../reducers/itemSlice";
import { setUser } from "../reducers/userSlice";
import { addNewItemRequest, addNewListRequest, fetchItemsOfListRequest, fetchUserInfoRequest } from "./Requests"
import { useDispatch } from "react-redux";

const AddNewItem = async(selectedListList_id, token) => {
    await addNewItemRequest(selectedListList_id, token);
    const response = await fetchItemsOfListRequest(selectedListList_id, token);
    console.log('Addnewitem',response);
    return response.data.items;
};

export default AddNewItem;