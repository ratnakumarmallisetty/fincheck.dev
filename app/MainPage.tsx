import React from 'react';
import './globals.css';

const MainPage = ({ onSignOut }: { onSignOut: () => void }) => {
  return (
    <div className="page-container">
      <button className="signout-button" onClick={onSignOut}>
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
          <polyline points="16 17 21 12 16 7"/>
          <line x1="21" y1="12" x2="9" y2="12"/>
        </svg>
        Sign Out
      </button>
      <div className="content-card">
        <h1 className="welcome-title">Welcome to the Main Page</h1>
        <p className="welcome-text">You have successfully signed in!</p>
      </div>
    </div>
  );
};

export default MainPage;