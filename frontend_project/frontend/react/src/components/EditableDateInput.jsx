import React, { useState, useRef } from 'react';
import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEdit } from '@fortawesome/free-solid-svg-icons';


function EditableDateInput({ initialValue, onSave }) {
    const [selectedDate, setSelectedDate] = useState(initialValue ? new Date(initialValue) : new Date());

    const handleDateChange = (date) => {
        setSelectedDate(date);
        onSave(formatDateForSave(date));
    };

    const formatDateForSave = (date) => {
        return date.toISOString().slice(0, 10);
    };

    return (
        <DatePicker
            selected={selectedDate}
            onChange={handleDateChange}
            dateFormat="M/d"
            className="form-control w-full text-center"
        />
    );
}

//inputフォームの共通化
function EditableInput({ initialValue, onSave, className='' }) {
    const [value, setValue] = useState(initialValue);
    const inputRef = useRef(null);
    const [isComposing, setIsComposing] = useState(false);

    const handleBlur = () => {
        if (!isComposing) {
            onSave(value);
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === "Enter" && !isComposing) {
            e.preventDefault();
            inputRef.current.blur();
        }
    };

    return (
        <input
            className={`focus:outline-none focus:ring-0 bg-white bg-opacity-0 ${className}`}
            ref={inputRef}
            type="text"
            value={value}
            onChange={e => setValue(e.target.value)}
            onBlur={handleBlur}
            onKeyDown={handleKeyDown}
            onCompositionStart={() => setIsComposing(true)}
            onCompositionEnd={() => {
                setIsComposing(false);
                onSave(value);
            }}
        />
    )
}



function EditableInputWithButton({ initialValue, onSave, onClick, showEditButton, className = '' }) {
    const [value, setValue] = useState(initialValue);
    const [isEditing, setIsEditing] = useState(false);
    const inputRef = useRef(null);
    const [isComposing, setIsComposing] = useState(false);

    const handleBlur = () => {
        if (!isComposing) {
            onSave(value);
            setIsEditing(false);
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === "Enter" && !isComposing) {
            e.preventDefault();
            inputRef.current.blur();
        }
    };

    const handleEditButtonClick = () => {
        setIsEditing(true);
        inputRef.current.focus();
    };

    const handleInputClick = () => {
        if (!isEditing && onClick) {
            onClick();
        }
    };

    return (
        <div className="flex items-center">
            <input
                className={`focus:outline-none focus:ring-0 bg-white bg-opacity-0 ${className}`}
                ref={inputRef}
                type="text"
                value={value}
                onChange={e => setValue(e.target.value)}
                onBlur={handleBlur}
                onKeyDown={handleKeyDown}
                onCompositionStart={() => setIsComposing(true)}
                onCompositionEnd={() => {
                    setIsComposing(false);
                    onSave(value);
                }}
                onClick={handleInputClick}
                readOnly={!isEditing}
            />
            {showEditButton && (
                <button onClick={handleEditButtonClick} className="ml-2">
                    <FontAwesomeIcon icon={faEdit} />
                </button>
            )}
        </div>
    )
}




export { EditableDateInput, EditableInput, EditableInputWithButton };
