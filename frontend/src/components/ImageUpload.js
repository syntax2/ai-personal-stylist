// // frontend/src/components/ImageUpload.js
// import React, { useState } from "react";

// function ImageUpload() {
//   const [selectedFile, setSelectedFile] = useState(null);
//   const [result, setResult] = useState(null);
//   const [loading, setLoading] = useState(false);

//   const handleFileChange = (e) => {
//     setSelectedFile(e.target.files[0]);
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     if (!selectedFile) {
//       alert("Please choose an image");
//       return;
//     }

//     setLoading(true);
//     setResult(null);
//     const formData = new FormData();
//     formData.append("file", selectedFile);

//     try {
//       const res = await fetch("http://localhost:8000/recommend", {
//         method: "POST",
//         body: formData,
//       });
//       const data = await res.json();
//       setResult(data);
//     } catch (err) {
//       console.error("Error:", err);
//       alert("Error uploading image");
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <form onSubmit={handleSubmit} className="space-y-6">
//       <input
//         type="file"
//         accept="image/*"
//         onChange={handleFileChange}
//         className="block w-full text-sm text-gray-800 border border-gray-300 rounded-lg cursor-pointer focus:outline-none p-2 bg-gray-100"
//       />
//       <button
//         type="submit"
//         className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded transition-colors duration-300"
//       >
//         {loading ? "Processing..." : "Upload & Get Style Recommendation"}
//       </button>
//       {result && (
//         <div className="mt-8 text-center">
//           <h2 className="font-bold text-2xl mb-2">Analysis & Recommendation</h2>
//           <p className="mb-2">
//             Dominant Color:{" "}
//             <span style={{ color: result.analysis.hex_color }}>
//               {result.analysis.hex_color}
//             </span>
//           </p>
//           <p className="mb-2">{result.recommendation.description}</p>
//           {result.recommendation.affiliate_link && (
//             <a
//               href={result.recommendation.affiliate_link}
//               target="_blank"
//               rel="noopener noreferrer"
//               className="text-blue-400 underline hover:text-blue-300 transition-colors duration-300"
//             >
//               Check it out!
//             </a>
//           )}
//           <div
//             className="w-16 h-16 mx-auto mt-4 rounded border border-gray-700"
//             style={{ backgroundColor: result.analysis.hex_color }}
//           />
//         </div>
//       )}
//     </form>
//   );
// }

// export default ImageUpload;

import React, { useState, useRef } from "react";

function ImageUpload({ isDarkMode, setResult }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setError(null);

    if (file) {
      // Check file type
      const validTypes = ["image/jpeg", "image/png", "image/heic"];
      if (!validTypes.includes(file.type)) {
        setError("Please select a JPG, PNG, or HEIC file");
        return;
      }

      // Check file size (10MB)
      if (file.size > 10 * 1024 * 1024) {
        setError("File size must be less than 10MB");
        return;
      }

      setSelectedFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const triggerFileInput = () => {
    fileInputRef.current.click();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedFile) {
      setError("Please select an image first");
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch("http://localhost:8000/recommend", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error("Error:", err);
      setError("Failed to process image. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="space-y-4">
          <input
            type="file"
            ref={fileInputRef}
            accept="image/jpeg,image/png,image/heic"
            onChange={handleFileChange}
            className="hidden"
          />

          {!preview ? (
            <div
              onClick={triggerFileInput}
              className={`border-2 border-dashed rounded-lg p-12 flex flex-col items-center justify-center cursor-pointer transition-all duration-300 ${
                isDarkMode
                  ? "border-gray-600 hover:border-blue-500 bg-gray-800/40"
                  : "border-gray-300 hover:border-blue-500 bg-gray-50"
              }`}
            >
              <div
                className={`p-4 rounded-full mb-4 ${
                  isDarkMode ? "bg-gray-700" : "bg-gray-100"
                }`}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  className={isDarkMode ? "text-blue-400" : "text-blue-500"}
                >
                  <path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"></path>
                  <circle cx="12" cy="13" r="3"></circle>
                </svg>
              </div>
              <p className="font-medium mb-1">Click to upload an image</p>
              <p
                className={`text-xs ${
                  isDarkMode ? "text-gray-400" : "text-gray-500"
                }`}
              >
                JPG, PNG, or HEIC up to 10MB
              </p>
            </div>
          ) : (
            <div className="relative rounded-lg overflow-hidden">
              <img
                src={preview}
                alt="Preview"
                className="w-full h-64 object-cover"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent pointer-events-none"></div>

              <button
                type="button"
                onClick={() => {
                  setPreview(null);
                  setSelectedFile(null);
                  setError(null);
                }}
                className="absolute top-2 right-2 bg-black/60 text-white p-2 rounded-full hover:bg-black/80 transition-colors"
                aria-label="Remove image"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              </button>

              <div className="absolute bottom-0 left-0 right-0 p-3 text-white bg-gradient-to-t from-black/80 to-transparent">
                <p className="text-sm font-medium truncate">
                  {selectedFile?.name}
                </p>
              </div>
            </div>
          )}

          {error && (
            <div
              className={`p-3 text-sm rounded ${
                isDarkMode
                  ? "bg-red-900/30 text-red-300"
                  : "bg-red-50 text-red-600"
              }`}
            >
              <div className="flex items-center">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  className="mr-2"
                >
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="12" y1="8" x2="12" y2="12"></line>
                  <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
                {error}
              </div>
            </div>
          )}
        </div>

        <button
          type="submit"
          disabled={loading || !selectedFile}
          className={`w-full py-3 px-4 rounded-lg text-white font-medium transition-all ${
            loading || !selectedFile
              ? "bg-blue-400 opacity-60 cursor-not-allowed"
              : "bg-blue-600 hover:bg-blue-700 shadow-lg hover:shadow-blue-600/30"
          }`}
        >
          {loading ? (
            <div className="flex items-center justify-center">
              <svg
                className="animate-spin -ml-1 mr-2 h-5 w-5 text-white"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                ></circle>
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
              Processing Image...
            </div>
          ) : (
            <div className="flex items-center justify-center">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="mr-2"
              >
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="7 10 12 15 17 10"></polyline>
                <line x1="12" y1="15" x2="12" y2="3"></line>
              </svg>
              Get Style Recommendation
            </div>
          )}
        </button>
      </form>
    </div>
  );
}

export default ImageUpload;
