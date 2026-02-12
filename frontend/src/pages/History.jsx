import { useEffect, useState } from "react";
import { fetchQuizzes, fetchQuizDetail } from "../api/api.js";
import QuizModal from "../components/QuizModal.jsx";

const History = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [selectedQuiz, setSelectedQuiz] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setError("");
      try {
        const data = await fetchQuizzes();
        setItems(data);
      } catch (err) {
        console.error(err);
        setError("Failed to load history.");
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const openDetail = async (id) => {
    try {
      const data = await fetchQuizDetail(id);
      setSelectedQuiz(data);
      setModalOpen(true);
    } catch (err) {
      console.error(err);
      setError("Failed to load quiz details.");
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold text-slate-50">History</h1>
        {loading && (
          <span className="text-xs text-slate-400">Loading quizzes...</span>
        )}
      </div>
      {error && <p className="text-xs text-red-400">{error}</p>}
      <div className="overflow-hidden rounded-xl border border-slate-800 bg-slate-900/80">
        <table className="min-w-full divide-y divide-slate-800 text-xs">
          <thead className="bg-slate-900/90">
            <tr>
              <th className="px-4 py-2 text-left font-medium text-slate-300">
                Article
              </th>
              <th className="px-4 py-2 text-left font-medium text-slate-300">
                URL
              </th>
              <th className="px-4 py-2 text-left font-medium text-slate-300">
                Created
              </th>
              <th className="px-4 py-2 text-right font-medium text-slate-300">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800 bg-slate-900/50">
            {items.length === 0 && !loading && (
              <tr>
                <td
                  colSpan={4}
                  className="px-4 py-6 text-center text-slate-400"
                >
                  No quizzes yet. Generate one from the Generate tab.
                </td>
              </tr>
            )}
            {items.map((item) => (
              <tr key={item.id}>
                <td className="px-4 py-2 text-slate-100">
                  {item.article_title}
                </td>
                <td className="px-4 py-2">
                  <a
                    href={item.article_url}
                    target="_blank"
                    rel="noreferrer"
                    className="truncate text-[11px] text-indigo-300 hover:text-indigo-200"
                  >
                    {item.article_url}
                  </a>
                </td>
                <td className="px-4 py-2 text-slate-300">
                  {new Date(item.created_at).toLocaleString()}
                </td>
                <td className="px-4 py-2 text-right">
                  <button
                    onClick={() => openDetail(item.id)}
                    className="rounded-md bg-slate-800 px-3 py-1 text-[11px] text-slate-100 hover:bg-slate-700"
                  >
                    Details
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <QuizModal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        quizDetail={selectedQuiz}
      />
    </div>
  );
};

export default History;

