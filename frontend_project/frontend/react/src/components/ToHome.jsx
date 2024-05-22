import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faHouse, faHouseCircleExclamation } from '@fortawesome/free-solid-svg-icons';

function ToHomeButton({ userInfo, handleToHome }) {
    return (
        <>
            {userInfo.invitation ? (
                <button onClick={handleToHome}>
                    <FontAwesomeIcon icon={faHouseCircleExclamation} style={{ color: "#ff6524", fontSize: '32px' }} />
                </button>
            ) : (
                <button onClick={handleToHome}>
                    <FontAwesomeIcon icon={faHouse} style={{ color: "#075ef2", fontSize: '32px' }} />
                </button>
            )}
        </>

    );
}

export default ToHomeButton;
