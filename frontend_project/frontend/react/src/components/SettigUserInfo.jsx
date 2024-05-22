import { useSelector } from "react-redux";
import { EditableInput } from "./EditableDateInput";
import LineLinkBtn from "../utils/LineLink";


function SettingUserInfo () {
    const userInfo = useSelector(state => state.user);

    return(
        <>
        <div className="relative mb-6 border-b w-full">
            <label className="absolute -top-2.5 left-2  px-1 text-xs text-gray-600">アイコン</label>
            <EditableInput initialValue={userInfo.user_id} onSave={""} className="text-xl text-center" />
        </div>
        <div className="relative mb-6 border-b w-80">
            <label className="absolute -top-2.5 left-2  px-1 text-xs text-gray-600">ユーザー名</label>
            <EditableInput initialValue={userInfo.user_name} onSave={""} className="text-xl text-center" />
        </div>
        <div className="relative mb-6 border-b w-80">
            <label className="absolute -top-2.5 left-2 w-full px-1 text-xs text-gray-600">メールアドレス</label>
            <EditableInput initialValue={userInfo.email} onSave={""} className="text-xl text-center" />
        </div>
        <div className="relative mb-6 border-b w-80">
            <label className="absolute -top-2.5 left-2  px-1 text-xs text-gray-600">最初に開く画面</label>
            <EditableInput initialValue={userInfo.default_list} onSave={""} className="text-xl text-center" />
        </div>
        <div className="relative mb-6 border-b w-80">
            <label className="absolute -top-2.5 left-2  px-1 text-xs text-gray-600">LINE連携</label>
            <EditableInput initialValue={userInfo.line_status} onSave={""} className="text-xl text-center" />
        </div>

        <LineLinkBtn />
        <div className="relative mb-6 border-b w-80">
            <label className="absolute -top-2.5 left-2  px-1 text-xs text-gray-600">LINE通知する</label>
            <EditableInput initialValue={userInfo.remind} onSave={""} className="text-xl text-center" />
        </div>
        <div className="relative mb-6 border-b w-80">
            <label className="absolute -top-2.5 left-2  px-1 text-xs text-gray-600">通知する時刻</label>
            <EditableInput initialValue={userInfo.remind_time} onSave={""} className="text-xl text-center" />
        </div>
        <div className="relative mb-6 border-b w-80">
            <label className="absolute -top-2.5 left-2  px-1 text-xs text-gray-600">通知するタイミング</label>
            <EditableInput initialValue={userInfo.remind_timing} onSave={""} className="text-xl text-center" />
        </div>
        </>
    )
}

export default SettingUserInfo;