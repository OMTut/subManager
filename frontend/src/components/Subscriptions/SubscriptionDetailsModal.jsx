import React, { useState, useEffect } from 'react';
import DeleteButton from '../Buttons/DeleteButton';
import '../../styles/detailsSubscriptionsModal.css';


const SubscriptionDetailsModal = ({ subscription, onClose, onUpdate, onDelete, refresh, showMessage }) => {
    const [subscriptionData, setSubscriptionData] = useState(subscription);
    const [originalSubscription] = useState(subscription);
    const [isEditing, setIsEditing] = useState(false);
    const [formData, setFormData] = useState({
        name: subscription.name,
        price: subscription.price,
        category: subscription.category,
        account: subscription.account
    })

    const handleStatusChange = (updatedSubscription) => {
        // Update local state with the received updated subscription
        setSubscriptionData(updatedSubscription);
    }

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await updateSubscription(subscription.account, formData);
            setIsEditing(false);
            setSubscriptionData(formData);
            if (refresh) refresh();
            if (onUpdate) onUpdate();
            if (showMessage) showMessage('Subscription updated successfully', 'success');
        } catch (error) {
            if (showMessage) showMessage('Failed to update subscription', 'error');
        }
    };
    
    const handleClose = async () => {
        try {
            
            // Refresh the parent component
            if (refresh) {
                refresh();
            }
            
            // Close the modal
            onClose();
        } catch (error) {
            console.error('Error saving subscription changes:', error);
            if (showMessage) {
                showMessage('Failed to save changes', 'error');
            }
        }
    }
    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <div className="modal-close">
                    <button 
                        type="button"
                        className="modal-close-button"
                        onClick={handleClose}
                        aria-label="Close modal"
                    >×
                    </button>
                </div>
                {isEditing ? (
                    <form onSubmit={handleSubmit}>
                        <div className="form-group">
                            <label htmlFor="name">Name:</label>
                            <input
                                type="text"
                                id="name"
                                name="name"
                                value={formData.name}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="price">Price:</label>
                            <input
                                type="text"
                                id="price"
                                name="price"
                                value={formData.price}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="category">Category:</label>
                            <input
                                type="text"
                                id="category"
                                name="category"
                                value={formData.category}
                                onChange={handleChange}
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="account">Account:</label>
                            <input
                                type="text"
                                id="account"
                                name="account"
                                value={formData.account_holder}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="form-actions">
                            <button type="button" className="cancel-button" 
                                onClick={() => {
                                    setIsEditing(false);
                                    onClose();
                                }}>
                                Cancel
                            </button>
                            <button type="submit" className="save-button">Save</button>
                        </div>
                    </form>
                ) : (
                    <>
                        <div className="modal-header">
                            <h2>{subscriptionData.name}</h2>
                        </div>
                        <div className="subscription-details">
                            <p><strong>Price:</strong> {subscriptionData.price}</p>
                            <p><strong>Category:</strong> {subscriptionData.category}</p>
                            <p><strong>Account:</strong> {subscriptionData.account_holder}</p>
                            <p><strong>Email:</strong> {subscriptionData.account_email}</p>
                        </div>
                        <div className='subscription-operations'>
                            <button 
                                className="edit-button" 
                                onClick={() => setIsEditing(true)}
                            >
                                Edit
                            </button>
                            <DeleteButton 
                                id={subscriptionData.id}
                                onDeleteSuccess={() => {
                                    onClose();
                                    onUpdate && onUpdate();
                                    onDelete && onDelete();
                                    refresh && refresh();
                                }}
                            />
                        </div>
                    </>
                )}
            </div>
                
                
        </div>
    );
};

export default SubscriptionDetailsModal;