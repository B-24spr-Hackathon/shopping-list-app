import { setSelectedList } from "../reducers/selectedListSlice";
import { setUser } from "../reducers/userSlice";
import { addNewListRequest, fetchUserInfoRequest } from "../utils/Requests"
import { useDispatch, useSelector } from "react-redux";

function AddNewList() {
    const dispatch = useDispatch();
    const token = useSelector(state => state.token.token);

    const handleAddNewList = async() => {
        const newListResponse = await addNewListRequest(token);
        const userInfo = await fetchUserInfoRequest(token);
        dispatch(setUser({lists: userInfo.data.lists}));
        dispatch(setSelectedList({...newListResponse.data, is_owner: true}));

    }
    return (
        <button
            className="text-sm mb-1"
            onClick={handleAddNewList}>
            
            ＋新しいリストを作成する
        </button>

    )

}

export default AddNewList;