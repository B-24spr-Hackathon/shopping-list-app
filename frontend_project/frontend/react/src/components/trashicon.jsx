import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTrash } from '@fortawesome/free-solid-svg-icons';

export function TrashBtn( { onClick } ) {
    return (
        <button onClick={onClick}>
            <FontAwesomeIcon icon={faTrash} style={{color:'rgba(185, 50, 0, 1)'}} />
        </button>
    );
}