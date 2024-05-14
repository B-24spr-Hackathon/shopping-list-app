import React, { useState } from 'react';
import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";

function EditableDateInput({ initialValue, onSave }) {
    const [selectedDate, setSelectedDate] = useState(initialValue ? new Date(initialValue) : new Date());

    const handleDateChange = (date) => {
        setSelectedDate(date);
        onSave(formatDate(date));
    };

    const formatDate = (date) => {
        return date.toISOString().slice(0, 10);
    };

    return (
        <DatePicker
            selected={selectedDate}
            onChange={handleDateChange}
            dateFormat="yyyy-MM-dd"
            className="form-control"
        />
    );
}

export default EditableDateInput;
