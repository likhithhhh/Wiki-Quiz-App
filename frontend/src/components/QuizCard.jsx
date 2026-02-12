const QuizCard = ({ article, quiz, onTakeQuiz }) => {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/70 p-4 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h3 className="text-lg font-semibold text-slate-50">{article.title}</h3>
          <p className="mt-1 text-xs text-slate-400 line-clamp-3">
            {article.summary || "No summary available."}
          </p>
          <a
            href={article.url}
            target="_blank"
            rel="noreferrer"
            className="mt-2 inline-flex text-xs text-indigo-400 hover:text-indigo-300"
          >
            View article
          </a>
        </div>
        <span className="rounded-full bg-slate-800 px-3 py-1 text-xs text-slate-300">
          {quiz.questions.length} questions
        </span>
      </div>
      <button
        onClick={onTakeQuiz}
        className="mt-4 inline-flex items-center rounded-md bg-emerald-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-emerald-500"
      >
        Take quiz
      </button>
    </div>
  );
};

export default QuizCard;

