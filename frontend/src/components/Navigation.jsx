const Navigation = ({ onSelectView }) => {
    return (
       <nav>
          <ul>
             <li><a href="#" id="link1" 
                onClick={() => onSelectView('home')}>Home</a>
             </li>
             <li><a href="#" id="link1" 
                onClick={() => onSelectView('subscriptions')}>Subscriptions</a>
             </li>
          </ul>
       </nav>
    );
 };
 
 export default Navigation;