"use client";

import { useState } from "react";

export default function MainPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  async function handleSubmit(e: React.MouseEvent<HTMLButtonElement>) {
    e.preventDefault();

    if (!selectedFile) {
      alert("Please select an image ");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const res = await fetch("http://127.0.0.1:8000/upload-image", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      if (!res.ok) {
        alert(`Upload failed ❌: ${data.detail}`);
        return;
      }

      alert("Uploaded successfully 🎉");
      console.log("📌 SERVER RESPONSE:", data);
      setSelectedFile(null);
    } catch (err) {
      console.error(err);
      alert("Server error, try again later ");
    }
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen gap-10 bg-gradient-to-br from-gray-900 to-teal-800 p-10">
      <h1 className="text-4xl font-black text-white text-center">
        Bank Document <br /> Submission Portal
      </h1>

      {/* File Input */}
      <label className="text-white font-medium flex flex-col gap-3 items-center cursor-pointer">
        <span className="text-lg">Choose an Image:</span>
        <input
          type="file"
          accept="image/*"
          className="block w-full text-sm text-white file:border-none file:bg-teal-500 file:cursor-pointer file:text-white file:rounded-lg file:px-4 file:py-2"
          onChange={(e) => setSelectedFile(e.target.files?.[0] ?? null)}
        />
      </label>

      {/* Submit Button */}
      <button
        type="button"
        onClick={handleSubmit}
        className="bg-teal-500 hover:bg-teal-600 active:bg-teal-700 text-white font-bold py-3 px-8 rounded-xl shadow-lg transition-all duration-150"
      >
        Submit Image
      </button>
    </div>
  );
}
