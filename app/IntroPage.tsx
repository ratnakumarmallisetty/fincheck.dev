import React, { useState } from 'react';
import "./globals.css"

const IntroPage = ({ onEnter }: { onEnter: () => void }) => {
  return (
    <div className="page-container">
      <div className="content-card">
        <h1 className="main-title">Final Year Project</h1>
        <div className="info-section">
          <p className="group-label">Group 73</p>
          <div className="member-list">
            <p className="member-id">CSE22363</p>
            <p className="member-id">CSE22505</p>
            <p className="member-id">CSE22526</p>
            <p className="member-id">CSE22531</p>
          </div>
        </div>
        <button className="primary-button" onClick={onEnter}>
          Enter
        </button>
      </div>
    </div>
  );
};

export default IntroPage;