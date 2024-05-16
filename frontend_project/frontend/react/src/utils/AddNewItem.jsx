import { setItemAllInfo } from "../reducers/itemSlice";
import { setUser } from "../reducers/userSlice";
import { addNewItemRequest, addNewListRequest, fetchItemsOfListRequest, fetchUserInfoRequest } from "./Requests"
import { useDispatch } from "react-redux";

const AddNewItem = async(selectedListList_id) => {
    await addNewItemRequest(selectedListList_id);
    const response = await fetchItemsOfListRequest(selectedListList_id);
    console.log('res',response);
    return response.data.items;
};

export default AddNewItem;