const API_URL = import.meta.env.VITE_API_BASE_URL;

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

        // For DELETE operations, check if there's content before parsing JSON
        // HTTP 204 No Content responses have empty body
        if (response.status === 204 || response.headers.get('content-length') === '0') {
            return { success: true };
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error updating subscription:', error);
        throw error;
    }
};