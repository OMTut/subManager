import React, { useState, useEffect } from 'react';
import { updateSubscription } from '../../services/updateSubscription';
import DeleteButton from '../Buttons/DeleteButton';
import '../../styles/detailsSubscriptionsModal.css';


const SubscriptionDetailsModal = ({ subscription, onClose, onUpdate, onDelete, refresh, showMessage }) => {
    const [subscriptionData, setSubscriptionData] = useState(subscription);
    const [originalSubscription] = useState(subscription);
    const [isEditing, setIsEditing] = useState(false);
    const [formData, setFormData] = useState({
        companyName: subscription.name,
        price: subscription.price,
        subscriptionCategory: subscription.category,
        description: subscription.description,
        userName: subscription.account_holder,
        emailAssociated: subscription.account_email
    })



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
            // Convert price to float to preserve decimal values
            const submitData = {
                ...formData,
                price: parseFloat(formData.price)
            };
            await updateSubscription(subscription.id, submitData);
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
                            <label htmlFor="companyName">Name:</label>
                            <input
                                type="text"
                                id="name"
                                name="companyName"
                                value={formData.companyName}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="price">Price:</label>
                            <input
                                type="number"
                                step="0.01"
                                min="0"
                                id="price"
                                name="price"
                                value={formData.price}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="subscriptionCategory">Category:</label>
                            <input
                                type="text"
                                id="subscriptionCategory"
                                name="subscriptionCategory"
                                value={formData.subscriptionCategory}
                                onChange={handleChange}
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="description">Description:</label>
                            <input
                                type="text"
                                id="description"
                                name="description"
                                value={formData.description}
                                onChange={handleChange}
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="userName">Account Holder:</label>
                            <input
                                type="text"
                                id="userName"
                                name="userName"
                                value={formData.userName}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="emailAssociated">Account Email:</label>
                            <input
                                type="text"
                                id="emailAssociated"
                                name="emailAssociated"
                                value={formData.emailAssociated}
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
                            <p><strong>Description:</strong> {subscriptionData.description}</p>
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