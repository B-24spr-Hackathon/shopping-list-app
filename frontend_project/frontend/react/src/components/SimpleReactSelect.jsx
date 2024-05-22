import React from 'react';
import Select, { components } from 'react-select';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCircle } from '@fortawesome/free-solid-svg-icons';

export const options = [
    { value: '0', label: <FontAwesomeIcon icon={faCircle} style={{color: "#ee2f2f", fontSize: "1.5rem"}} /> },
    { value: '1', label: <FontAwesomeIcon icon={faCircle} style={{color: "#ff00dd", fontSize: "1.5rem"}} /> },
    { value: '2', label: <FontAwesomeIcon icon={faCircle} style={{color: "#fa7000", fontSize: "1.5rem"}} /> },
    { value: '3', label: <FontAwesomeIcon icon={faCircle} style={{color: "#FFD43B", fontSize: "1.5rem"}} /> },
    { value: '4', label: <FontAwesomeIcon icon={faCircle} style={{color: "#63E6BE", fontSize: "1.5rem"}} /> },
    { value: '5', label: <FontAwesomeIcon icon={faCircle} style={{color: "#00a321", fontSize: "1.5rem"}} /> },
    { value: '6', label: <FontAwesomeIcon icon={faCircle} style={{color: "#74C0FC", fontSize: "1.5rem"}} /> },
    { value: '7', label: <FontAwesomeIcon icon={faCircle} style={{color: "#004cff", fontSize: "1.5rem"}} /> },
    { value: '8', label: <FontAwesomeIcon icon={faCircle} style={{color: "#B197FC", fontSize: "1.5rem"}} /> },
    { value: '9', label: <FontAwesomeIcon icon={faCircle} style={{color: "#811aff", fontSize: "1.5rem"}} /> },
    { value: '10', label: <FontAwesomeIcon icon={faCircle} style={{color: "#919191", fontSize: "1.5rem"}} /> },
];

const customStyles = {
    control: (provided) => ({
        ...provided,
        minHeight: '30px', // Smaller box height
        height: '30px',
        fontSize: '1rem', // Adjust font size
        width: '40px', // Adjust width
        backgroundColor: 'transparent', // Make background transparent
        border: 'none', // Optionally remove border
        boxShadow: 'none', // Optionally remove box shadow
    }),
    valueContainer: (provided) => ({
        ...provided,
        height: '30px',
        padding: '0 6px',
        backgroundColor: 'transparent', // Make background transparent
    }),
    input: (provided) => ({
        ...provided,
        margin: '0px',
        backgroundColor: 'transparent', // Make background transparent
    }),
    indicatorsContainer: (provided) => ({
        ...provided,
        height: '30px',
        backgroundColor: 'transparent', // Make background transparent
    }),
    option: (provided) => ({
        ...provided,
        fontSize: '1.0rem', // Larger font size for options
        height: '40px',
        backgroundColor: 'transparent', // Make background transparent
    }),
    menu: (provided) => ({
        ...provided,
        // backgroundColor: 'transparent', // Make background transparent
        zIndex: 9999, // Ensure the menu is on top of other elements
    }),
    menuPortal: (provided) => ({
        ...provided,
        zIndex: 9999, // Ensure the menu is on top of other elements
    }),
    singleValue: (provided) => ({
        ...provided,
        backgroundColor: 'transparent', // Make background transparent
    }),
    placeholder: (provided) => ({
        ...provided,
        backgroundColor: 'transparent', // Make background transparent
    }),
};

const NoInput = (props) => <components.Input {...props} readOnly />;

const SimpleSelectBox = ({ color, onChange }) => {
    const selectedOption = options.find(option => option.value == color);

    return (
        <div>
            <Select
                value={selectedOption}
                onChange={selectedOption => onChange(selectedOption)}
                options={options}
                styles={customStyles}
                components={{ DropdownIndicator: () => null, IndicatorSeparator: () => null, Input: NoInput }} // Remove the dropdown indicator and separator, and disable input cursor
                menuPortalTarget={document.body} // Render the menu in the body
            />
        </div>
    );
};

export default SimpleSelectBox;
