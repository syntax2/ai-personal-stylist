// frontend/src/components/ImageUpload.js
import React, { useState } from "react";

function ImageUpload() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedFile) {
      alert("Please choose an image");
      return;
    }

    setLoading(true);
    setResult(null);
    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      // Call the recommendation endpoint
      const res = await fetch("http://localhost:8000/recommend", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error("Error:", err);
      alert("Error uploading image");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        className="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer focus:outline-none"
      />
      <button
        type="submit"
        className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
      >
        {loading ? "Processing..." : "Upload & Get Style Recommendation"}
      </button>
      {result && (
        <div className="mt-4 text-center">
          <h2 className="font-bold text-xl">Analysis & Recommendation</h2>
          <p>
            Dominant Color:{" "}
            <span style={{ color: result.analysis.hex_color }}>
              {result.analysis.hex_color}
            </span>
          </p>
          <p>{result.recommendation.description}</p>
          {result.recommendation.affiliate_link && (
            <a
              href={result.recommendation.affiliate_link}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-500 underline"
            >
              Check it out!
            </a>
          )}
          <div
            className="w-16 h-16 mx-auto mt-2"
            style={{
              backgroundColor: result.analysis.hex_color,
              border: "1px solid #000",
            }}
          />
        </div>
      )}
    </form>
  );
}

export default ImageUpload;
