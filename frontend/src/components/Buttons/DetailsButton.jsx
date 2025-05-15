import React, { useState } from 'react';
import SubscriptionDetailsModal from '../Subscriptions/SubscriptionDetailsModal';

const DetailsButton = ({ subscription, showMessage, refresh }) => {
    const [showModal, setShowModal] = useState(false);

    const handleClose = () => {
        setShowModal(false);
    };

    return (
        <>
            <button
                onClick={() => setShowModal(true)}
                className="edit-button"
            >
                Details
            </button>
            {showModal && (
                <SubscriptionDetailsModal
                    subscription={subscription}
                    onClose={handleClose}
                    refresh={refresh}
                    showMessage={showMessage}
                />
            )}
        </>
    );
};

export default DetailsButton;