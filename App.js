import React, { useState } from "react";
import axios from "axios";
import "./index.css"; // Ensure this is correctly imported


function App() {
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    setLoading(true);
    setResponse(null);
    setError(null);

    try {
      const res = await axios.post("http://127.0.0.1:8000/generate-app/", { prompt });
      setResponse(res.data.data);
    } catch (error) {
      console.error("Error:", error);
      setError("Failed to fetch response. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-100 to-blue-300 p-6">
      <div className="w-full max-w-xl bg-white shadow-xl rounded-2xl p-8 text-center">
        <h1 className="text-3xl font-bold text-gray-800">🚀 AI Web Builder</h1>
        <p className="text-gray-600 mt-2">
          Enter an app idea, and AI will generate code for you!
        </p>

        {/* Input Form Centered */}
        <form onSubmit={handleSubmit} className="mt-6 flex flex-col items-center">
          <input
            type="text"
            placeholder="Enter your app idea..."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            className="w-3/4 p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-center"
          />
          <button
            type="submit"
            disabled={!prompt.trim() || loading}
            className="w-3/4 mt-3 bg-green-600 text-white py-3 rounded-lg font-semibold hover:bg-green-700 disabled:bg-gray-400 transition-all duration-300"
          >
            {loading ? "Generating..." : "Generate"}
          </button>
        </form>

        {/* Error Message */}
        {error && <p className="mt-4 text-red-500 text-sm">{error}</p>}

        {/* AI Response Display */}
        {response && (
          <div className="mt-6 p-5 bg-gray-100 border border-gray-300 rounded-lg shadow-md text-left">
            <h2 className="text-xl font-bold text-gray-800">{response.app_name}</h2>
            <p className="text-gray-700 mt-2">{response.description}</p>

            {/* Code Block (if available) */}
            {response.code && response.code !== "No code generated." && (
              <div className="mt-4">
                <h3 className="text-lg font-semibold text-gray-700">Generated Code:</h3>
                <pre className="text-sm text-white bg-gray-900 p-4 rounded-lg overflow-x-auto whitespace-pre-wrap">
                  <code className="font-mono">{response.code}</code>
                </pre>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
