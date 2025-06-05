import { useState } from 'react';
import useAddSubscription from '../../hooks/useAddSubscription';
import '../../styles/detailsSubscriptionsModal.css';


const AddSubscriptionModal = ({ onClose, onSubAdd }) => {
    const { handleAddSubscritpion, isLoading, error } = useAddSubscription();
    const [formData, setFormData] = useState({
        companyName: '',
        price: '',
        subscriptionCategory: '',
        description: '',
        userName: '',
        emailAssociated: ''
    });

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
            const newSubscription = await handleAddSubscritpion(submitData);
            onSubAdd(newSubscription);
            setFormData({
                companyName: '',
                price: '',
                subscriptionCategory: '',
                description: '',
                userName: '',
                emailAssociated: ''
            });
            onClose();
        } catch (err) {
            console.error('Error adding subscription:', err);
        }
    };

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <div className="modal-close">
                    <button 
                        type="button"
                        className="modal-close-button"
                        onClick={onClose}
                        aria-label="Close modal"
                    >×
                    </button>
                </div>
                
                <div className="modal-header">
                    <h2>Add New Subscription</h2>
                </div>
                
                {error && <div className="error-message">{error}</div>}
                
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="companyName">Company Name:</label>
                        <input 
                            type="text" 
                            id="companyName"
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
                        <textarea 
                            id="description"
                            name="description" 
                            value={formData.description} 
                            onChange={handleChange}
                            rows="3"
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
                        />
                    </div>
                    
                    <div className="form-group">
                        <label htmlFor="emailAssociated">Account Email:</label>
                        <input 
                            type="email" 
                            id="emailAssociated"
                            name="emailAssociated" 
                            value={formData.emailAssociated} 
                            onChange={handleChange} 
                        />
                    </div>
                    
                    <div className="form-actions">
                        <button type="button" className="cancel-button" onClick={onClose}>
                            Cancel
                        </button>
                        <button type="submit" className="save-button" disabled={isLoading}>
                            {isLoading ? 'Adding...' : 'Add Subscription'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default AddSubscriptionModal;