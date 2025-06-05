const API_URL = import.meta.env.VITE_API_BASE_URL;

export const addSubscription = async (subscriptionData) => {
    try {
        console.log('Adding subscription with data:', subscriptionData);
        const response = await fetch(`${API_URL}/subscriptions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(subscriptionData),
        });

        console.log('Response status:', response.status);
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || `Server responsed with status ${response.status}`);
        }

        console.log('Subscription added successfully:', data);
        return data;
    } catch (error) {
        console.error('Error adding subscription:', error);
        throw error;
    }
}