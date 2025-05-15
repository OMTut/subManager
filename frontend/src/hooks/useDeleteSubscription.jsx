import { useState } from 'react';
import { deleteSubscription } from '../services/deleteSubscription';

const useDeleteSubscription = (showMessage) => {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleDeleteSubscription = async (id, onSuccess) => {
        try {
            setIsLoading(true);
            setError(null);
            await deleteSubscription(id);
            console.log('Subscription deleted successfully');
            if (showMessage) {
                showMessage?.('Subscription deleted successfully!', 'success');
                console.log('Calling showMessage with success');
            }
            if (onSuccess && typeof onSuccess === 'function') {
                onSuccess();
            }
        } catch (err) {
            console.error('Error deleting subscription:', err);
            setError(err);
            if (showMessage) {
                showMessage?.('Failed to delete subscription', 'error');
            }
            return false;
        } finally {
            setIsLoading(false);
        }
    };

    return { handleDeleteSubscription, isLoading, error };
};

export default useDeleteSubscription;