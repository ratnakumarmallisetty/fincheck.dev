"use client";

import React, { useState } from "react";
import "./globals.css";

interface Props {
  onBack: () => void;
  onNavigateToSignIn: () => void;
}

const SignUpPage: React.FC<Props> = ({ onNavigateToSignIn, onBack }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const handleSubmit = async () => {
    setError("");

    if (!username || !password || !confirmPassword) {
      setError("Please fill in all fields");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters");
      return;
    }

    const res = await fetch("/api/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    if (!res.ok) {
      setError((await res.text()) || "Failed to create account");
      return;
    }

    alert("Account created! Please sign in.");
    onNavigateToSignIn();
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
        <h2 className="auth-title">Sign Up</h2>

        <div className="auth-form">
          <div className="form-group">
            <label className="form-label">Username</label>
            <input
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Choose a username"
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
                placeholder="Create a password"
                className="form-input"
              />
              <button type="button" className="eye-button" onClick={() => setShowPassword(!showPassword)}>
                {showPassword ? "🙈" : "👁️"}
              </button>
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Confirm Password</label>
            <div className="password-input-wrapper">
              <input
                type={showConfirmPassword ? "text" : "password"}
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Re-enter password"
                className="form-input"
              />
              <button type="button" className="eye-button" onClick={() => setShowConfirmPassword(!showConfirmPassword)}>
                {showConfirmPassword ? "🙈" : "👁️"}
              </button>
            </div>
          </div>

          {error && <div className="error-message">{error}</div>}

          <button className="primary-button" onClick={handleSubmit}>
            Sign Up
          </button>
        </div>

        <div className="auth-footer">
          <p className="footer-text">Already have an account?</p>
          <button className="link-button" onClick={onNavigateToSignIn}>
            Sign In
          </button>
        </div>
      </div>
    </div>
  );
};

export default SignUpPage;
