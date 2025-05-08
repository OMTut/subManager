

const RightColumn = ({ view = 'home' }) => {

   const renderContent = () => {
       switch(view) {
           case 'home':
               return (
                   <>
                       <h2>PlaceHolder - Home</h2>
                   </>
               );
               
           case 'subscriptions':
               return (
                   <>
                       <h2>Placeholder - Subscriptions</h2>
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