import { useGetAllSubscriptions } from "../hooks/useGetAllSubscriptions"
import AllSubscriptionsList from "./Subscriptions/SubscriptionList";


const RightColumn = ({ view = 'home' }) => {
    const { subscriptions: allSubscriptions, loading: allLoading, error: allError } = useGetAllSubscriptions();

   const LoadingSpinner = () => <div>Loading...</div>;
   const ErrorMessage = ({ error }) => <div>Error: {error}</div>;

   const renderContent = () => {
       switch(view) {
           case 'home':
               return (
                   <>
                       <h2>PlaceHolder - Home</h2>
                   </>
               );
               
            case 'subscriptions':
                if (allLoading) return <LoadingSpinner />;
                if (allError) return <ErrorMessage error={availableError} />;
                return (
                    <>
                        <AllSubscriptionsList books={allSubscriptions} />
                    </>
                );
               
           default:
               return <div>Select a view</div>;
       }
   };

   return (
       <div className="right-column">
           {renderContent()}
       </div>
   );
};

export default RightColumn;