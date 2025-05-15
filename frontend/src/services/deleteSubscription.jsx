const API_URL = 'http://localhost:8000';

export const deleteSubscription = async (id) => {
    try {
        const response = await fetch(`${API_URL}/subscriptions/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error updating subscription:', error);
        throw error;
    }
};