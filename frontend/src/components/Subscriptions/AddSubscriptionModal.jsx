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
            const newSubscription = await handleAddSubscritpion(formData);
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
                <h2>Add Subscription</h2>
                {error && <div className="error-message">{error}</div>}
                <form onSubmit={handleSubmit}>
                    <label>
                        Name:
                        <input type="text" name="companyName" value={formData.companyName} onChange={handleChange} required />
                    </label>
                    <label>
                        Price:
                        <input type="text" name="price" value={formData.price} onChange={handleChange} required />
                    </label>
                    <label>
                        Category:
                        <input type="text" name="subscriptionCategory" value={formData.subscriptionCategory} onChange={handleChange} />
                    </label>
                    <label>
                        Description:
                        <input type="textarea" name="description" value={formData.description} onChange={handleChange} />
                    </label>
                    <label>
                        Account Holder:
                        <input type="text" name="userName" value={formData.userName} onChange={handleChange} />
                    </label>
                    <label>
                        Account Email:
                        <input type="email" name="emailAssociated" value={formData.emailAssociated} onChange={handleChange} />
                    </label>
                    <button type="submit">Add Subscription</button>
                    <button type="button" onClick={onClose}>Cancel</button>
                </form>
            </div>
        </div>
    );
}

export default AddSubscriptionModal;