import { useState } from 'react';
import { useGetAllSubscriptions } from '../../hooks/useGetAllSubscriptions';
import SubscriptionCard from './SubscriptionCard';
import AddSubscriptionButton from '../Buttons/AddSubscriptionButton';
import MessageAlert from '../MessageAlert';
import useMessageAlert from '../../hooks/useMessageAlert'

const AllSubscriptionsList = () => {
    const { subscriptions, loading, error, refreshSubscriptions } = useGetAllSubscriptions();
    const { message, messageType, showMessage, clearMessage } = useMessageAlert();
    
    const handleSubscriptionAdded = () => {
        showMessage('Subscription added successfully!', 'success');
        refreshSubscriptions();
    };

    if (loading) { return <div className="loading">Loading subscriptions...</div>; }
    if (error) { return <div className="error">Error: {error}</div>; }

    if (!subscriptions || subscriptions.length === 0) { return <div className="no-subscriptions">No subscriptions available.</div>; }

    // Sort subscriptions by availability (available subscriptions first)
    const sortedSubscriptions = [...subscriptions].sort((a, b) => {
        //if (a.avail === b.avail) return 0;
        //return a.avail ? -1 : 1;
        return a.name.localeCompare(b.name, undefined, { sensitivity: 'base' });
    });

    // Calculate dashboard stats
    const totalSubscriptions = subscriptions.length;
    const totalCost = subscriptions.reduce((sum, sub) => sum + (parseFloat(sub.price) || 0), 0);

    return (
        <>
            <MessageAlert 
                message={message} 
                messageType={messageType} 
                onClear={clearMessage}
            />
            
            {/* Dashboard Stats */}
            <div className="dashboard-stats">
                <div className="stat-card">
                    <h3>Monthly Cost</h3>
                    <p className="stat-value">${totalCost.toFixed(2)}</p>
                </div>
                <div className="stat-card">
                    <h3>Total Subscriptions</h3>
                    <p className="stat-value">{totalSubscriptions}</p>
                </div>
            </div>

            <div className="subscription-container">
                <div className="subscription-container-header">
                    <h2>Your Subscriptions</h2>
                    <AddSubscriptionButton onSubAdd={handleSubscriptionAdded} />
                </div>
                <table className="subscription-list">
                    <thead>
                        <tr>
                            <th>Subscription</th>
                            <th>Price</th>
                            <th>Category</th>
                            <th>Account Holder</th>
                            <th>Account Email</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                <tbody>
                    {
                    sortedSubscriptions.map(subscription => (
                        <SubscriptionCard key={subscription.id} subscription={subscription} refresh={refreshSubscriptions} showMessage={showMessage}/>
                    ))
                    }
                </tbody>

                </table>
            </div>
        </>
    );
};

export default AllSubscriptionsList;