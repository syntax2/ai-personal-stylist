// // frontend/src/App.js
// import React from "react";
// import ImageUpload from "./components/ImageUpload";

// function App() {
//   return (
//     <div className="min-h-screen bg-gray-900 text-gray-100 flex items-center justify-center p-4">
//       <div className="bg-gray-800 rounded-xl shadow-2xl p-8 w-full max-w-md transform transition duration-500 hover:scale-105">
//         <h1 className="text-4xl font-extrabold mb-6 text-center tracking-wide">
//           AI Personal Stylist
//         </h1>
//         <ImageUpload />
//         <p className="mt-6 text-center text-sm opacity-70">
//           Get personalized style recommendations instantly.
//         </p>
//       </div>
//     </div>
//   );
// }

// export default App;
import React, { useState, useEffect } from "react";
import ImageUpload from "./components/ImageUpload";
import Results from "./components/Results";
import { Camera, Sparkles } from "lucide-react";

function App() {
  const [isDarkMode, setIsDarkMode] = useState(() => {
    // Get initial theme from localStorage or user preference
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme) {
      return savedTheme === "dark";
    }
    // Use system preference as fallback
    return window.matchMedia("(prefers-color-scheme: dark)").matches;
  });

  const [result, setResult] = useState(null);

  // Apply theme to document when it changes
  useEffect(() => {
    document.documentElement.classList.toggle("dark", isDarkMode);
    localStorage.setItem("theme", isDarkMode ? "dark" : "light");
  }, [isDarkMode]);

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
  };

  return (
    <div
      className={`min-h-screen transition-colors duration-300 ${
        isDarkMode ? "bg-gray-900 text-gray-100" : "bg-gray-50 text-gray-800"
      }`}
    >
      <header className="px-4 py-4 shadow-sm bg-opacity-80 backdrop-blur-sm fixed top-0 left-0 right-0 z-10">
        <div className="container mx-auto flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <Camera className="text-blue-500" size={24} />
            <h1
              className={`text-xl font-bold ${
                isDarkMode ? "text-white" : "text-gray-900"
              }`}
            >
              AI Personal Stylist
            </h1>
          </div>
          <button
            onClick={toggleTheme}
            className={`p-2 rounded-full transition-colors ${
              isDarkMode
                ? "bg-gray-800 hover:bg-gray-700"
                : "bg-gray-200 hover:bg-gray-300"
            }`}
            aria-label={
              isDarkMode ? "Switch to light mode" : "Switch to dark mode"
            }
          >
            {isDarkMode ? (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="text-yellow-400"
              >
                <circle cx="12" cy="12" r="5"></circle>
                <line x1="12" y1="1" x2="12" y2="3"></line>
                <line x1="12" y1="21" x2="12" y2="23"></line>
                <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                <line x1="1" y1="12" x2="3" y2="12"></line>
                <line x1="21" y1="12" x2="23" y2="12"></line>
                <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
              </svg>
            ) : (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="text-blue-600"
              >
                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
              </svg>
            )}
          </button>
        </div>
      </header>

      <main className="container mx-auto px-4 pt-24 pb-12">
        <section className="max-w-lg mx-auto">
          {/* Hero section */}
          <div className="text-center mb-8">
            <h2
              className={`text-3xl md:text-4xl font-bold mb-4 ${
                isDarkMode ? "text-white" : "text-gray-900"
              }`}
            >
              Discover Your Perfect Style
            </h2>
            <p
              className={`text-lg ${
                isDarkMode ? "text-gray-300" : "text-gray-600"
              }`}
            >
              Upload your photo and get AI-powered style recommendations
              tailored just for you.
            </p>
          </div>

          {/* Main card */}
          <div
            className={`rounded-xl shadow-xl overflow-hidden transition-all duration-300 ${
              isDarkMode
                ? "bg-gray-800 shadow-gray-950/50"
                : "bg-white shadow-gray-200/70"
            }`}
          >
            {/* Feature highlight bar */}
            <div
              className={`p-4 flex items-center text-sm ${
                isDarkMode
                  ? "bg-blue-900/20 text-blue-300"
                  : "bg-blue-50 text-blue-700"
              }`}
            >
              <Sparkles size={16} className="mr-2" />
              <p>
                AI-powered analysis for personalized fashion recommendations
              </p>
            </div>

            {/* Upload section */}
            <div className="p-6">
              <ImageUpload isDarkMode={isDarkMode} setResult={setResult} />
            </div>

            {/* Privacy note */}
            <div
              className={`px-6 pb-6 text-center text-xs ${
                isDarkMode ? "text-gray-400" : "text-gray-500"
              }`}
            >
              Your images are processed securely and privately.
            </div>
          </div>

          {/* Results section */}
          {result && (
            <div className="mt-8">
              <Results isDarkMode={isDarkMode} result={result} />
            </div>
          )}
        </section>
      </main>

      <footer
        className={`py-6 text-center text-sm ${
          isDarkMode ? "text-gray-400" : "text-gray-500"
        }`}
      >
        © {new Date().getFullYear()} AI Personal Stylist • All rights reserved
      </footer>
    </div>
  );
}

export default App;
