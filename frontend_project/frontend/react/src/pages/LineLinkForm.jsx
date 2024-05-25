import React, { useState } from "react";
import { useSelector } from "react-redux";
import { Header } from "../components/HeaderImg";
import { LineBtn } from "../components/Buttons";

function LineLinkForm () {
    const [copySuccess, setCopySuccess] = useState('');
    const lineLinkInfo = useSelector(state => state.lineLink)
    let displayText = lineLinkInfo.otp.substring(0, 10)


    const copyToClipboard = () => {
        navigator.clipboard.writeText(lineLinkInfo.otp).then(() => {
          setCopySuccess('コピー成功!');
        }, () => {
          setCopySuccess('コピーに失敗しました。');
        });
      };
    return(
        <>
        <div>

            <Header/>
            <div className="flex justify-center mt-24">
                <img className="w-52 h-40 object-cover rounded-full" src="/kaimotto.jpeg"/>
            </div>

            <div className="flex justify-center items-center flex-col my-16">
                <a href={lineLinkInfo.url}>
                    <LineBtn children="LINE連携はこちら" />
                </a>
            <div>
                <div className="flex justify-center">
                    {displayText}...
                </div>

                <button onClick={copyToClipboard}>ここを押してコピー</button>
            </div>
            <div className="flex justify-center mt-8">
                {copySuccess && <p>{copySuccess}</p>}

            </div>
            </div>
        </div>
        </>
    )
}

export default LineLinkForm;