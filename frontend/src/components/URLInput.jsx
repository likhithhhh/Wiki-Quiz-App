import { useState } from "react";

const URLInput = ({ onSubmit, loading }) => {
  const [url, setUrl] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");
    try {
      const parsed = new URL(url);
      if (!parsed.hostname.includes("wikipedia.org")) {
        setError("Please enter a valid Wikipedia article URL.");
        return;
      }
      onSubmit(url);
    } catch {
      setError("Please enter a valid URL.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <label className="block text-sm font-medium text-slate-200">
        Wikipedia article URL
      </label>
      <input
        type="url"
        className="w-full rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 placeholder-slate-500 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
        placeholder="https://en.wikipedia.org/wiki/Alan_Turing"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />
      {error && <p className="text-xs text-red-400">{error}</p>}
      <button
        type="submit"
        disabled={loading}
        className="inline-flex items-center rounded-md bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {loading ? "Generating..." : "Generate quiz"}
      </button>
    </form>
  );
};

export default URLInput;

