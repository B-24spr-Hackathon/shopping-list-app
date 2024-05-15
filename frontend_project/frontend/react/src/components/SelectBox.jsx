import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { fetchItemsOfListRequest } from "../utils/Requests";
import { useDispatch } from "react-redux";
import { clearSelectedList, setSelectedList } from "../reducers/selectedListSlice";
import { setItemAllInfo, clearItem } from "../reducers/itemSlice.jsx";


function SelectList() {
    const list = useSelector(state => state.user.lists);
    const selectedList = useSelector(state => state.selectedList)
    const dispatch = useDispatch();

    // useEffect(() => {
    //     if(list.length > 0) {
    //         dispatch(setSelectedList({
    //             list_id: list[0].list_id,
    //             list_name: list[0].list_name
    //         }));
    //     } else {
    //         dispatch(clearSelectedList());
    //     }
    // }, [list, dispatch]);

    const handleSelectChange = async(event) => {
        const selected = list.find(item => item.list_id == event.target.value);
        dispatch(setSelectedList({
            list_id: selected.list_id,
            list_name: selected.list_name
        }));
        
        const response = await fetchItemsOfListRequest(selected.list_id);
        console.log(response.data.list_id);
        console.log(response.data.items);
        dispatch(setItemAllInfo(response.data.items))
    }

    return (
        <>
            <div>
                <select 
                    value={selectedList.list_id}
                    onChange={handleSelectChange}>
                    {list.map((item, index) => (
                        <option key={index} value={item.list_id}>
                            {item.list_name}{item.list_id}{index}
                        </option>
                    ))}
                </select>
            </div>
        </>
    );

}

export { SelectList };