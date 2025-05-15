/**
 * SubscriptionCard component displays a card with subscription information
 * @param {Object} props - Component props
 * @param {Object} props.subscription - subscription object
 * @param {number} props.subscription.id - subscription object
 * @param {string} props.subscription.name - name of the subscription
 * @param {string} props.subscription.price - price of the subscription
 * @param {string} [props.subscription.category] - category of the subscription (optional)
 * @param {string} [props.subscription.account_holder] - account holder of the subscription (optional)
 *  * @param {string} [props.subscription.account_email] - account holder of the subscription (optional)
 * @returns {JSX.Element} subscription card component
 */
import DetailsButton from "../Buttons/DetailsButton"

const SubscriptionCard = ({ subscription, refresh, showMessage }) => {
    return (
        <tr key={subscription.id}>
            <td>{subscription.name}</td>
            <td>{subscription.price}</td>
            <td>{subscription.category || 'N/A'}</td>
            <td>{subscription.account_holder || 'N/A'}</td>
            <td>{subscription.account_email || 'N/A'}</td>
            <td>
                <DetailsButton 
                    subscription={subscription} 
                    showMessage={showMessage}
                    refresh={refresh}
                />
            </td>
        </tr>
    );
};

export default SubscriptionCard;