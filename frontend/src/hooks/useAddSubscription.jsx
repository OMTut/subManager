import { useState } from 'react';
import { addSubscription } from '../services/addSubscription';
import useMessageAlert from './useMessageAlert';

const useAddSubscription = () => {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setErrro] = useState(null);
    const { showMessage } = useMessageAlert();

    const handleAddSubscritpion = async (subData) => {
        setIsLoading(true);
        setErrro(null);

        try {
            const newSubscription = await addSubscription(subData);
            console.log('Subscription added successfully:', newSubscription);
            showMessage('Subscription added successfully!', 'success');
            return newSubscription;
        } catch (err) {
            console.error('Error adding subscription:', err)
            showMessage('Failed to add subscription', 'error');
            return false
        } finally {
            setIsLoading(false);
        }
    }
    return { handleAddSubscritpion, isLoading, error };
}

export default useAddSubscription;