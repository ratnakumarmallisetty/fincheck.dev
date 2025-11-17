"use client";

import React, { useState } from "react";
import { signIn } from "next-auth/react";
import "./globals.css";

interface Props {
  onSignIn: () => void;
  onNavigateToSignUp: () => void;
  onBack: () => void;
}

const SignInPage: React.FC<Props> = ({ onSignIn, onNavigateToSignUp, onBack }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = async () => {
    setError("");

    if (!username || !password) {
      setError("Please fill in all fields");
      return;
    }

    const res = await signIn("credentials", {
      username,
      password,
      redirect: false,
    });

    if (res?.error) {
      setError("Invalid username or password");
      return;
    }

    onSignIn();
  };

  return (
    <div className="page-container">
      <button className="back-button" onClick={onBack}>
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M19 12H5M12 19l-7-7 7-7" />
        </svg>
        Back
      </button>

      <div className="auth-card">
        <h2 className="auth-title">Sign In</h2>

        <div className="auth-form">
          <div className="form-group">
            <label className="form-label">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter your username"
              className="form-input"
            />
          </div>

          <div className="form-group">
            <label className="form-label">Password</label>
            <div className="password-input-wrapper">
              <input
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
                className="form-input"
              />

              <button
                type="button"
                className="eye-button"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? "🙈" : "👁️"}
              </button>
            </div>
          </div>

          {error && <div className="error-message">{error}</div>}

          <button className="primary-button" onClick={handleSubmit}>
            Sign In
          </button>
        </div>

        <div className="auth-footer">
          <p className="footer-text">Don't have an account?</p>
          <button className="link-button" onClick={onNavigateToSignUp}>
            Sign Up
          </button>
        </div>
      </div>
    </div>
  );
};

export default SignInPage;
