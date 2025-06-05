const API_URL = import.meta.env.VITE_API_URL;

export const getAllSubscriptions = async () => {
    try {
        console.log('Fetching all subscriptions from API...');
        const response = await fetch(`${API_URL}/subscriptions`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`)
        }
            
        const responseData = await response.json();
        return responseData;
    } catch (error) {
        console.error('Error fetching all subscriptions:', error);
        throw error;
    }
}