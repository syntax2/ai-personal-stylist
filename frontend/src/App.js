// frontend/src/App.js
import React from "react";
import ImageUpload from "./components/ImageUpload";

function App() {
  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center text-gray-100">
      <div className="bg-gray-800 p-8 rounded shadow-lg w-full max-w-md">
        <h1 className="text-3xl font-bold mb-6 text-center">
          AI Personal Stylist
        </h1>
        <ImageUpload />
      </div>
    </div>
  );
}

export default App;
