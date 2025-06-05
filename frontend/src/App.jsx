import { useState } from 'react'
import './styles/layout1.css'
import './styles/navigation.css'
import Header from './components/Header'
import Footer from './components/Footer'
import Sidebar from './components/Sidebar'
import RightColumn from './components/RightColumn'

function App() {
  const [currentView, setCurrentView] = useState('subscriptions');

  const handleViewSelect = (view) => {
    setCurrentView(view);
  };

  return (
    <div className="container">
       <Header />
       <div className="left-column">
         <Sidebar onViewSelect={handleViewSelect} currentView={currentView} />
       </div>
       <div className="right-column">
         <RightColumn view={currentView}/>
       </div>
       <Footer />
   </div>
 );
}

export default App
