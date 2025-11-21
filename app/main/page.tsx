import React, { useState } from 'react';
import './globals.css';

const MainPage = ({ onSignOut }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [details, setDetails] = useState('');
  const [isDragging, setIsDragging] = useState(false);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  const handleSubmit = () => {
    if (selectedFile && details.trim()) {
      alert('Document submitted successfully!');
      setSelectedFile(null);
      setDetails('');
    } else {
      alert('Please upload a document and provide details.');
    }
  };

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

      <div className="portal-container">
        <h1 className="portal-heading">Bank Document Submission Portal</h1>
        
        <div>
          <div
            className={`upload-area ${isDragging ? 'dragging' : ''}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => document.getElementById('fileInput').click()}
          >
            <svg className="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
              <polyline points="17 8 12 3 7 8"/>
              <line x1="12" y1="3" x2="12" y2="15"/>
            </svg>
            <p className="upload-text">Upload Your Document</p>
            <p className="upload-subtext">Drag and drop or click to browse</p>
            <input
              id="fileInput"
              type="file"
              className="file-input"
              onChange={handleFileChange}
              accept=".pdf,.doc,.docx,.jpg,.jpeg,.png"
            />
            <button type="button" className="select-file-button">
              Select File
            </button>
            
            {selectedFile && (
              <div className="selected-file">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#4a7c87" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/>
                  <polyline points="13 2 13 9 20 9"/>
                </svg>
                <span>{selectedFile.name}</span>
              </div>
            )}
          </div>

          <div className="details-group">
            <label className="details-label">Important Details</label>
            <textarea
              className="details-textarea"
              placeholder="Enter account number, document type, purpose, or any additional information..."
              value={details}
              onChange={(e) => setDetails(e.target.value)}
            />
          </div>

          <button onClick={handleSubmit} className="submit-document-button">
            Submit Document
          </button>
        </div>
      </div>
    </div>
  );
};

export default MainPage;