import React, { useState } from "react";
import { useSelector } from "react-redux";

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
            <div>
                <a href={lineLinkInfo.url}>LINE連携はこちら</a>
            </div>
            <div>
                <div>
                    {displayText}...
                </div>

                <button onClick={copyToClipboard}>コピー</button>
            </div>
        {copySuccess && <p>{copySuccess}</p>}
        </div>
        </>
    )
}

export default LineLinkForm;