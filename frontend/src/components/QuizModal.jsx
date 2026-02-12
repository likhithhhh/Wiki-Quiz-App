import { useState } from "react";

const QuizModal = ({ isOpen, onClose, quizDetail }) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);

  if (!isOpen || !quizDetail) return null;

  const questions = quizDetail.quiz.questions;
  const currentQuestion = questions[currentIndex];

  const handleSelect = (questionIdx, optionText) => {
    if (submitted) return;
    setAnswers((prev) => ({ ...prev, [questionIdx]: optionText }));
  };

  const handleNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex((idx) => idx + 1);
    }
  };

  const handlePrev = () => {
    if (currentIndex > 0) {
      setCurrentIndex((idx) => idx - 1);
    }
  };

  const handleSubmit = () => {
    setSubmitted(true);
  };

  const handleClose = () => {
    setCurrentIndex(0);
    setAnswers({});
    setSubmitted(false);
    onClose();
  };

  const correctCount = submitted
    ? questions.reduce(
        (acc, q, idx) => (answers[idx] === q.correct_answer ? acc + 1 : acc),
        0
      )
    : 0;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70">
      <div className="max-h-[90vh] w-full max-w-2xl overflow-hidden rounded-2xl bg-slate-900 shadow-xl">
        <div className="flex items-center justify-between border-b border-slate-800 px-5 py-3">
          <div>
            <h2 className="text-sm font-semibold text-slate-100">
              {quizDetail.article.title}
            </h2>
            <p className="text-xs text-slate-400">
              Question {currentIndex + 1} of {questions.length}
            </p>
          </div>
          <button
            onClick={handleClose}
            className="rounded-full bg-slate-800 px-2 py-1 text-xs text-slate-300 hover:bg-slate-700"
          >
            Close
          </button>
        </div>
        <div className="space-y-4 px-5 py-4">
          <p className="text-sm font-medium text-slate-100">
            {currentQuestion.question}
          </p>
          <div className="space-y-2">
            {currentQuestion.options.map((opt, idx) => {
              const selected = answers[currentIndex] === opt.text;
              const isCorrect = submitted && opt.text === currentQuestion.correct_answer;
              const isWrong =
                submitted &&
                selected &&
                opt.text !== currentQuestion.correct_answer;
              return (
                <button
                  key={idx}
                  type="button"
                  onClick={() => handleSelect(currentIndex, opt.text)}
                  className={[
                    "flex w-full items-center justify-between rounded-md border px-3 py-2 text-left text-xs",
                    selected && !submitted
                      ? "border-indigo-500 bg-indigo-500/10"
                      : "border-slate-700 bg-slate-800/70",
                    isCorrect
                      ? "border-emerald-500 bg-emerald-500/10"
                      : "",
                    isWrong ? "border-red-500 bg-red-500/10" : "",
                  ]
                    .filter(Boolean)
                    .join(" ")}
                >
                  <span className="text-slate-100">{opt.text}</span>
                  {isCorrect && (
                    <span className="text-[10px] font-semibold text-emerald-400">
                      Correct
                    </span>
                  )}
                  {isWrong && (
                    <span className="text-[10px] font-semibold text-red-400">
                      Incorrect
                    </span>
                  )}
                </button>
              );
            })}
          </div>
          {submitted && (
            <div className="rounded-md bg-slate-800/70 px-3 py-2 text-xs text-slate-200">
              <p className="font-semibold">
                Score: {correctCount} / {questions.length}
              </p>
              <p className="mt-1 text-slate-400">
                Explanation: {currentQuestion.explanation || "No explanation provided."}
              </p>
            </div>
          )}
        </div>
        <div className="flex items-center justify-between border-t border-slate-800 px-5 py-3 text-xs">
          <div className="space-x-2">
            <button
              onClick={handlePrev}
              disabled={currentIndex === 0}
              className="rounded-md bg-slate-800 px-3 py-1 text-slate-200 disabled:opacity-40"
            >
              Previous
            </button>
            <button
              onClick={handleNext}
              disabled={currentIndex === questions.length - 1}
              className="rounded-md bg-slate-800 px-3 py-1 text-slate-200 disabled:opacity-40"
            >
              Next
            </button>
          </div>
          {!submitted ? (
            <button
              onClick={handleSubmit}
              className="rounded-md bg-indigo-600 px-4 py-1.5 font-semibold text-white hover:bg-indigo-500"
            >
              Submit quiz
            </button>
          ) : (
            <button
              onClick={handleClose}
              className="rounded-md bg-slate-700 px-4 py-1.5 font-semibold text-slate-100 hover:bg-slate-600"
            >
              Close
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default QuizModal;

