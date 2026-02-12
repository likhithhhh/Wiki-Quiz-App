import { useState } from "react";
import GenerateQuiz from "./pages/GenerateQuiz.jsx";
import History from "./pages/History.jsx";

const App = () => {
  const [tab, setTab] = useState("generate");

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <header className="border-b border-slate-800 bg-slate-950/80 backdrop-blur">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-3">
          <div className="flex items-center gap-2">
            <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-indigo-600 text-xs font-bold">
              WQ
            </div>
            <div>
              <h1 className="text-sm font-semibold">Wiki Quiz App</h1>
              <p className="text-[11px] text-slate-400">
                Generate MCQ quizzes from Wikipedia articles.
              </p>
            </div>
          </div>
          <nav className="flex gap-2 text-xs">
            <button
              onClick={() => setTab("generate")}
              className={[
                "rounded-full px-3 py-1",
                tab === "generate"
                  ? "bg-slate-800 text-slate-50"
                  : "text-slate-400 hover:bg-slate-900",
              ].join(" ")}
            >
              Generate quiz
            </button>
            <button
              onClick={() => setTab("history")}
              className={[
                "rounded-full px-3 py-1",
                tab === "history"
                  ? "bg-slate-800 text-slate-50"
                  : "text-slate-400 hover:bg-slate-900",
              ].join(" ")}
            >
              History
            </button>
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-5xl px-4 py-6">
        {tab === "generate" ? <GenerateQuiz /> : <History />}
      </main>
    </div>
  );
};

export default App;

