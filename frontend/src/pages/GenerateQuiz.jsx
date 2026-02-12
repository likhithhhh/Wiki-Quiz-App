import { useState } from "react";
import { generateQuiz } from "../api/api.js";
import URLInput from "../components/URLInput.jsx";
import QuizCard from "../components/QuizCard.jsx";
import QuizModal from "../components/QuizModal.jsx";

const GenerateQuiz = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);

  const handleGenerate = async (url) => {
    setLoading(true);
    setError("");
    try {
      const data = await generateQuiz(url);
      setResult(data);
      setModalOpen(true);
    } catch (err) {
      console.error(err);
      setError(
        err?.response?.data?.detail ||
          "Failed to generate quiz. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="rounded-xl border border-slate-800 bg-slate-900/80 p-5 shadow-sm">
        <h1 className="text-xl font-semibold text-slate-50">Generate quiz</h1>
        <p className="mt-1 text-xs text-slate-400">
          Paste a Wikipedia article URL to generate multiple-choice questions
          with explanations and difficulty ratings.
        </p>
        <div className="mt-4">
          <URLInput onSubmit={handleGenerate} loading={loading} />
        </div>
        {error && (
          <p className="mt-3 text-xs text-red-400">
            {error.toString()}
          </p>
        )}
      </div>

      {result && (
        <div>
          <h2 className="mb-3 text-sm font-semibold text-slate-100">
            Latest quiz
          </h2>
          <QuizCard
            article={result.article}
            quiz={result.quiz}
            onTakeQuiz={() => setModalOpen(true)}
          />
        </div>
      )}

      <QuizModal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        quizDetail={result}
      />
    </div>
  );
};

export default GenerateQuiz;

