import React, { useState } from 'react';
import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";

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

export default EditableDateInput;
