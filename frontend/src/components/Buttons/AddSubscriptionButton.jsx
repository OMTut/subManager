import { useState } from 'react';
import AddSubscriptionModal from '../Subscriptions/AddSubscriptionModal';

const AddSubscriptionButton = ({ onSubAdd }) => {
    const [showModal, setShowModal] = useState(false);

    const handleClick = () => {
        setShowModal(true);
    }
    const handleClose = () => {
        setShowModal(false);
    }

    return (
        <>
            <button
                onClick = { handleClick }
                className="btn btn-primary add-button"
            >
                + Add Subscription
            </button>
            {showModal && (
                <AddSubscriptionModal
                    onClose={handleClose}
                    onSubAdd={onSubAdd}
                />
            )}
        </>
    );
}

export default AddSubscriptionButton;