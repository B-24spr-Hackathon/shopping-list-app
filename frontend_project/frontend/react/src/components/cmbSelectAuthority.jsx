import React from 'react';

function PermissionDropdown({ value, onChange }) {
    return (
        <select value={value} onChange={onChange}>
            <option value="True">編集可</option>
            <option value="False">閲覧のみ</option>
        </select>
    );
}

export default PermissionDropdown;