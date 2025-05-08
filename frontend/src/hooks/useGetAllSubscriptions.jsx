import { useState, useEffect } from 'react';
import { getAllSubscriptions } from '../services/getAllSubscriptions';

export const useGetAllSubscriptions = () => {
    const [subscriptions, setSubscriptions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchSubscriptions = async () => {
        try {
            setLoading(true);
            const data = await getAllSubscriptions();
            setSubscriptions(data);
            setError(null);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchSubscriptions();
    }, []);

    return {
        subscriptions,
        loading,
        error,
        refreshSubscriptions: fetchSubscriptions
    };
}