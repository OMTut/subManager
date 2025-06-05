const API_URL = import.meta.env.VITE_API_BASE_URL;

export async function updateSubscription(subscriptionId, updatedData) {
    try {
        console.log('Updating subscription with data:', updatedData);
        console.log('Price type:', typeof updatedData.price, 'Price value:', updatedData.price);
        const response = await fetch(`${API_URL}/subscriptions/${subscriptionId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedData),
        });

        if (!response.ok) {
            throw new Error(`Error updating subscription: ${response.statusText}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Failed to update subscription:', error);
        throw error;
    }
}