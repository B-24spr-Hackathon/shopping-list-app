import React, {useRef} from 'react';
import { useDispatch, useSelector } from "react-redux";
import { EditableInput } from "./EditableDateInput";
import LineLinkBtn from "../utils/LineLink";
import { fetchUserInfoRequest, updateUserInfoRequest } from '../utils/Requests';
import { setUser } from '../reducers/userSlice';
import DropUserBtn from '../utils/DropUser';

function SettingUserInfo() {
    const userInfo = useSelector(state => state.user);
    const token = useSelector(state => state.token.token);
    const dispatch = useDispatch();
    const fileInputRef = useRef(null)

    const handleUpdateUserInfo = async (key, newValue) => {
        await updateUserInfoRequest(key, newValue, token);
        const userInfoResponse = await fetchUserInfoRequest(token);
        dispatch(setUser(userInfoResponse.data.user));
    };

    const handleFileChange = async (event) => {
        const file = event.target.files[0];
        if (file) {
            const formData = new FormData();
            formData.append('icon', file);

            try {
                // const response = await axios.post('/api/upload-icon', formData, {
                //     headers: {
                //         'Content-Type': 'multipart/form-data',
                //         'Authorization': `Bearer ${token}`
                //     }
                // });
                handleUpdateUserInfo('icon', response.data.filePath);
            } catch (error) {
                console.error("Error uploading the file", error);
            }
        }
    };

    const timeOptions = [];
    for (let h = 0; h < 24; h++) {
        for (let m = 0; m < 60; m += 10) {
            const hour = h.toString().padStart(2, '0');
            const minute = m.toString().padStart(2, '0');
            const time = `${hour}:${minute}`;
            timeOptions.push(time);
        }
    }

    const dayOptions = [];
    for (let d = 0; d <= 10; d++) {
        dayOptions.push(d);
    }

    const handleTimeChange = (event) => {
        const newValue = event.target.value;
        handleUpdateUserInfo('remind_time', newValue);
    };

    const handleTimingChange = (event) => {
        const newValue = event.target.value;
        handleUpdateUserInfo('remind_timing', newValue);
    };

    const handleRemindChange = (event) => {
        const newValue = event.target.value === 'true';
        handleUpdateUserInfo('remind', newValue);
    };

    const handleDefaultListChange = (event) => {
        const newValue = event.target.value === 'true';
        handleUpdateUserInfo('default_list', newValue);
    };

    return (
        <div className="flex flex-col items-center text-center">
            {/* <div className="relative mb-6 border-b w-full max-w-xs">
                <label className="absolute -top-2.5 left-2 px-1 text-xs text-gray-600">アイコン</label>
                <div className="mt-2 text-xl text-center">
                    <img
                        src={userInfo.icon}
                        alt="User Icon"
                        className="w-16 h-16 rounded-full mx-auto cursor-pointer"
                        onClick={() => fileInputRef.current.click()}
                    />
                    <input
                        type="file"
                        ref={fileInputRef}
                        onChange={handleFileChange}
                        style={{ display: 'none' }}
                    />
                </div>
            </div> */}
            <div className="relative mb-6 border-b w-full max-w-xs">
                <label className="absolute -top-2.5 left-2 px-1 text-xs text-gray-600">ユーザー名</label>
                <EditableInput initialValue={userInfo.user_name} onSave={(newValue => handleUpdateUserInfo('user_name',newValue))} className="text-xl mt-2 text-center" />
            </div>
            <div className="relative mb-6 border-b w-full max-w-xs">
                <label className="absolute -top-2.5 left-2 px-1 text-xs text-gray-600">ユーザーID</label>
                <EditableInput disabled='false' initialValue={userInfo.user_id} onSave={(newValue => handleUpdateUserInfo('user_id',newValue))} className="text-xl mt-2 text-center" />
            </div>

            {!userInfo.line_status && (
                <div className="relative mb-6 border-b w-full max-w-xs">
                    <label className="absolute -top-2.5 left-2 px-1 text-xs text-gray-600">メールアドレス</label>
                    <EditableInput
                        initialValue={userInfo.email}
                        onSave={(newValue) => handleUpdateUserInfo('email', newValue)}
                        className="w-full text-lg mt-2 text-center"
                    />
                </div>
            )}
            {/* <div className="relative mb-6 border-b w-full max-w-xs">
                <label className="absolute -top-2.5 left-2 px-1 text-xs text-gray-600">メールアドレス</label>
                <EditableInput initialValue={userInfo.email} onSave={(newValue => handleUpdateUserInfo('email',newValue))} className="w-full text-lg mt-2 text-center" />
            </div> */}
            <div className="relative mb-6 border-b w-full max-w-xs">
                <label className="absolute -top-2.5 left-2 px-1 text-xs text-gray-600">最初に開く画面</label>
                <div className="flex justify-center mt-2">
                    <label className="mr-4">
                        <input
                            type="radio"
                            name="default_list"
                            value="true"
                            checked={userInfo.default_list === true}
                            onChange={handleDefaultListChange}
                        />
                        商品管理
                    </label>
                    <label>
                        <input
                            type="radio"
                            name="default_list"
                            value="false"
                            checked={userInfo.default_list === false}
                            onChange={handleDefaultListChange}
                        />
                        お買い物リスト
                    </label>
                </div>
            </div>
            <div>
                <p>{userInfo.line_status ? "LINE連携済みです！" : "LINEと連携していると通知が受け取れます！"}</p>
            </div>
            <div className="relative mb-6  w-full max-w-xs">
                <LineLinkBtn />
            </div>
            <div className='text-gray-500 text-xs mb-4'>
                {userInfo.line_status ? "" : "以下はLINEと連携すると設定できます。"}
            </div>
            <div className="relative mb-6 border-b w-full max-w-xs">
                <label className="absolute -top-2.5 left-2 px-1 text-xs text-gray-600">LINE通知する</label>
                <div className="flex justify-center mt-2">
                    <label className="mr-4">
                        <input
                            type="radio"
                            name="remind"
                            value="true"
                            checked={userInfo.remind === true}
                            onChange={handleRemindChange}
                            disabled={!userInfo.line_status}
                        />
                        する
                    </label>
                    <label>
                        <input
                            type="radio"
                            name="remind"
                            value="false"
                            checked={userInfo.remind === false}
                            onChange={handleRemindChange}
                            disabled={!userInfo.line_status}
                        />
                        しない
                    </label>
                </div>
            </div>
            <div className="relative mb-6 border-b w-full max-w-xs">
                <label className="absolute -top-2.5 left-2 px-1 text-xs text-gray-600">通知する時刻</label>
                <select
                    value={userInfo.remind_time}
                    onChange={handleTimeChange}
                    className="mt-2 text-xl text-center w-32 bg-transparent border-none focus:outline-none"
                    disabled={!userInfo.line_status}
                >
                    {timeOptions.map((time, index) => (
                        <option key={index} value={time} className="text-sm">
                            {time}
                        </option>
                    ))}
                </select>
            </div>
            <div className="relative mb-2 border-b w-full max-w-xs">
                <label className="absolute -top-2.5 left-2 px-1 text-xs text-gray-600">通知するタイミング</label>
                <select
                    value={userInfo.remind_timing}
                    onChange={handleTimingChange}
                    className="mt-2 text-xl text-center w-24 bg-transparent border-none focus:outline-none"
                    disabled={!userInfo.line_status}
                >
                    {dayOptions.map((day, index) => (
                        <option key={index} value={day} className="text-sm">
                            {day} 日後
                        </option>
                    ))}
                </select>
            </div>
                    <div className="left-2 px-1 text-xs w-full max-w-xs text-start text-gray-600">　※お買い物リストに追加されていない場合、</div>
                    <div className="left-2 px-1 text-xs w-full max-w-xs text-start text-gray-600 mb-8">　　設定した日が経過すると通知がきます。</div>
            <DropUserBtn />
        </div>
    );
}

export default SettingUserInfo;
