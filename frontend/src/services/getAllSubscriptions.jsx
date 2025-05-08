const API_URL = 'http://localhost:8000';

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