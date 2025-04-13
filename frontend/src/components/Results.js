import React from "react";

function Results({ isDarkMode, result }) {
  if (!result) return null;

  const { analysis, recommendation } = result;

  // Helper function to determine if a color is light or dark
  const isLightColor = (hexColor) => {
    // Remove # if present
    const hex = hexColor.replace("#", "");

    // Convert hex to RGB
    const r = parseInt(hex.substr(0, 2), 16);
    const g = parseInt(hex.substr(2, 2), 16);
    const b = parseInt(hex.substr(4, 2), 16);

    // Calculate perceived brightness (common formula)
    const brightness = (r * 299 + g * 587 + b * 114) / 1000;

    // Return true if color is light
    return brightness > 125;
  };

  const textColorForSwatch = isLightColor(analysis.hex_color)
    ? "text-gray-800"
    : "text-white";

  return (
    <div
      className={`rounded-xl shadow-xl overflow-hidden transition-all duration-300 ${
        isDarkMode
          ? "bg-gray-800 shadow-gray-950/50"
          : "bg-white shadow-gray-200/70"
      }`}
    >
      <div
        className={`px-6 py-4 ${isDarkMode ? "bg-gray-700/50" : "bg-gray-50"}`}
      >
        <h2 className="text-xl font-bold">Your Style Analysis</h2>
      </div>

      <div className="p-6">
        {/* Color analysis */}
        <div className="flex items-center mb-6">
          <div
            className="w-16 h-16 rounded-lg shadow-lg mr-4 flex items-center justify-center"
            style={{ backgroundColor: analysis.hex_color }}
          >
            <span className={`text-xs font-mono ${textColorForSwatch}`}>
              {analysis.hex_color}
            </span>
          </div>
          <div>
            <h3 className="text-lg font-medium mb-1">Color Profile</h3>
            <p className={isDarkMode ? "text-gray-300" : "text-gray-600"}>
              Your dominant color tone
            </p>
          </div>
        </div>

        {/* Style profile */}
        {analysis.style_profile && (
          <div
            className={`p-4 rounded-lg mb-6 ${
              isDarkMode ? "bg-gray-700/50" : "bg-gray-50"
            }`}
          >
            <h3 className="font-medium mb-2">Style Profile</h3>
            <div className="flex items-center">
              <div
                className={`w-2 h-2 rounded-full mr-2 ${
                  isDarkMode ? "bg-blue-400" : "bg-blue-500"
                }`}
              ></div>
              <p>{analysis.style_profile}</p>
            </div>
          </div>
        )}

        {/* Recommendation */}
        <div
          className={`p-5 rounded-lg border ${
            isDarkMode
              ? "border-gray-700 bg-gray-700/30"
              : "border-gray-100 bg-blue-50/50"
          }`}
        >
          <h3
            className={`text-lg font-medium mb-3 ${
              isDarkMode ? "text-blue-300" : "text-blue-700"
            }`}
          >
            Recommendation
          </h3>
          <p className="mb-4">{recommendation.description}</p>

          {recommendation.affiliate_link && (
            <a
              href={recommendation.affiliate_link}
              target="_blank"
              rel="noopener noreferrer"
              className={`inline-flex items-center px-4 py-2 rounded-lg font-medium transition-colors ${
                isDarkMode
                  ? "bg-blue-600 hover:bg-blue-700 text-white"
                  : "bg-blue-600 hover:bg-blue-700 text-white"
              }`}
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
                className="mr-2"
              >
                <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
                <line x1="3" y1="6" x2="21" y2="6"></line>
                <path d="M16 10a4 4 0 0 1-8 0"></path>
              </svg>
              Shop This Look
            </a>
          )}
        </div>
      </div>

      <div
        className={`px-6 py-4 text-sm border-t ${
          isDarkMode
            ? "border-gray-700 text-gray-400"
            : "border-gray-100 text-gray-500"
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
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
          </svg>
          Based on AI analysis of your image
        </div>
      </div>
    </div>
  );
}

export default Results;
