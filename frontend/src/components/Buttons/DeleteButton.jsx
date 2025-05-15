import React from 'react';
import useDeleteSubscription from '../../hooks/useDeleteSubscription';

const DeleteButton = ({ id, onDeleteSuccess, showMessage }) => {
    const { handleDeleteSubscription, isLoading, error } = useDeleteSubscription(showMessage);

    const handleClick = async () => {
        await handleDeleteSubscription(id, onDeleteSuccess);
    };

    return (
        <div>
            {error && <div className="error-message">{error}</div>}
            <button
                onClick={handleClick}
                disabled={isLoading}
                className="delete-button"
            >
                {isLoading ? 'Deleting...' : 'Delete'}
            </button>
        </div>
    );
};

export default DeleteButton;