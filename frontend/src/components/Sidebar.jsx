import React from 'react';

const Sidebar = ({ onViewSelect, currentView }) => {
    return (
        <div className="sidebar">
            <nav className="sidebar-nav">
                <button 
                    className={`nav-item ${currentView === 'subscriptions' ? 'active' : ''}`}
                    onClick={() => onViewSelect('subscriptions')}
                    title="Subscriptions"
                >
                    <svg className="nav-icon" viewBox="0 0 24 24" fill="none">
                        <rect x="2" y="3" width="20" height="14" rx="2" stroke="currentColor" strokeWidth="2"/>
                        <line x1="8" y1="21" x2="16" y2="21" stroke="currentColor" strokeWidth="2"/>
                        <line x1="12" y1="17" x2="12" y2="21" stroke="currentColor" strokeWidth="2"/>
                    </svg>
                </button>
                
                <button 
                    className={`nav-item ${currentView === 'categories' ? 'active' : ''}`}
                    onClick={() => onViewSelect('categories')}
                    title="Categories"
                >
                    <svg className="nav-icon" viewBox="0 0 24 24" fill="none">
                        <rect x="3" y="3" width="7" height="7" rx="1" stroke="currentColor" strokeWidth="2"/>
                        <rect x="14" y="3" width="7" height="7" rx="1" stroke="currentColor" strokeWidth="2"/>
                        <rect x="14" y="14" width="7" height="7" rx="1" stroke="currentColor" strokeWidth="2"/>
                        <rect x="3" y="14" width="7" height="7" rx="1" stroke="currentColor" strokeWidth="2"/>
                    </svg>
                </button>
            </nav>
        </div>
    );
};

export default Sidebar;

