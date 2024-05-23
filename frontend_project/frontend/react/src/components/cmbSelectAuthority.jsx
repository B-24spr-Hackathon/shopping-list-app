import React from 'react';

function PermissionDropdown({ value, onChange }) {
    return (
        <select className='' value={value} onChange={onChange}>
            <option value="True">編集可</option>
            <option value="False">閲覧のみ</option>
        </select>
    );
}
function PermissionDropdownForMyListModal({ value, onChange }) {
    return (
        <select value={value} onChange={onChange} className='border rounded-lg'>
            <option value="true">編集可</option>
            <option value="false">閲覧のみ</option>
        </select>
    );
}

export { PermissionDropdown, PermissionDropdownForMyListModal };