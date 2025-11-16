'use client'

import React, { useState } from 'react';
import IntroPage from './IntroPage';
import SignInPage from './SignInPage';
import SignUpPage from './SignUpPage';
import MainPage from './MainPage';
import "./globals.css"

const App = () => {
  const [currentPage, setCurrentPage] = useState('intro');

  return (
    <>
      <div className="app">
        {currentPage === 'intro' && (
          <IntroPage onEnter={() => setCurrentPage('signin')} />
        )}
        {currentPage === 'signin' && (
          <SignInPage
            onSignIn={() => setCurrentPage('main')}
            onNavigateToSignUp={() => setCurrentPage('signup')}
            onBack={() => setCurrentPage('intro')}
          />
        )}
        {currentPage === 'signup' && (
          <SignUpPage
            onSignUp={() => setCurrentPage('main')}
            onNavigateToSignIn={() => setCurrentPage('signin')}
            onBack={() => setCurrentPage('intro')}
          />
        )}
        {currentPage === 'main' && <MainPage onSignOut={() => setCurrentPage('intro')} />}
      </div>
      
    </>
  );
};

export default App;