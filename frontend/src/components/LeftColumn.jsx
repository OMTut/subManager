import Navigation from "./Navigation";

const LeftColumn = ( {onSelectView }) => {
   return (
      <>
         <Navigation onSelectView={onSelectView}/>
      </>
   );
};

export default LeftColumn;