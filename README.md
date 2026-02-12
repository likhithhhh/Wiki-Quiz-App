## Wiki Quiz App

Wiki Quiz App is a full-stack application that turns Wikipedia articles into multiple-choice quizzes using FastAPI, PostgreSQL, BeautifulSoup, LangChain, and Gemini, with a React + Tailwind CSS frontend.

### Backend stack

- **FastAPI** (Python)
- **PostgreSQL** with **SQLAlchemy**
- **BeautifulSoup** for scraping Wikipedia HTML
- **LangChain** + **Gemini** (via `langchain-google-genai`)
- **Pydantic** for request/response schemas

### Frontend stack

- **React** (Vite)
- **Tailwind CSS**
- **Axios**

---

### Project structure

- **Backend (`app/`)**
  - `main.py` – FastAPI app factory, CORS, router registration, table creation
  - `config.py` – environment configuration (Gemini and database)
  - `database.py` – SQLAlchemy engine, session, and declarative base
  - `models/`
    - `article_model.py` – `Article` table
    - `quiz_model.py` – `Quiz` table
  - `schemas/`
    - `article_schema.py` – article and scraping Pydantic models
    - `quiz_schema.py` – quiz and API Pydantic models
  - `services/`
    - `scraper_service.py` – validate URL and scrape Wikipedia using BeautifulSoup
    - `entity_extractor.py` – lightweight heuristic entity extraction
    - `llm_service.py` – LangChain + Gemini quiz and related topics generation
    - `quiz_service.py` – orchestrates scraping, LLM calls, persistence, and history
  - `routers/`
    - `quiz_router.py` – `POST /generate-quiz`, `GET /generate-quiz/{id}`
    - `history_router.py` – `GET /quizzes`
  - `prompts/`
    - `quiz_prompt.txt` – prompt template for quiz generation
    - `related_topics_prompt.txt` – prompt template for related topics

- **Frontend (`frontend/`)**
  - `index.html` – app shell
  - `vite.config.mts` – Vite config
  - `tailwind.config.cjs`, `postcss.config.cjs`
  - `src/`
    - `main.jsx` – React bootstrapping
    - `index.css` – Tailwind and base styles
    - `App.jsx` – layout + tab navigation
    - `api/api.js` – Axios client and API helpers
    - `pages/`
      - `GenerateQuiz.jsx` – Tab 1: URL input and latest quiz view
      - `History.jsx` – Tab 2: history table + modal details
    - `components/`
      - `URLInput.jsx` – validated Wikipedia URL input
      - `QuizCard.jsx` – summary card for a generated quiz
      - `QuizModal.jsx` – “take quiz” mode with scoring and explanations

- **Other**
  - `requirements.txt` – Python dependencies
  - `sample_data/sample_quiz_response.json` – example backend response

---

### Environment variables

Create a `.env` file in the project root for the backend with:

```env
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/wiki_quiz
FRONTEND_ORIGIN=http://localhost:5173
```

> **Note:** `GEMINI_API_KEY` and `DATABASE_URL` are required; `FRONTEND_ORIGIN` defaults to `http://localhost:5173` if omitted.

For the frontend, you can optionally create `frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

---

### Database setup (PostgreSQL)

1. Start PostgreSQL locally and create a database:

```bash
createdb wiki_quiz
```

2. Ensure your `DATABASE_URL` in `.env` points to this database.

3. Tables are created automatically on app startup using SQLAlchemy metadata:
   - `articles`
   - `quizzes`

For production, you can introduce Alembic migrations, but they are not required to run this project.

---

### Backend setup and run

From the project root:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Run the FastAPI server with Uvicorn:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Key API endpoints:

- `POST /generate-quiz`  
  Body: `{"url": "https://en.wikipedia.org/wiki/Alan_Turing"}`  
  Response: article metadata, quiz (5–10 MCQs), related topics; saved to PostgreSQL.

- `GET /quizzes`  
  Returns a list of previous quizzes with article titles, URLs, and timestamps.

- `GET /generate-quiz/{id}`  
  Returns full quiz details (article + all questions + related topics) by quiz ID.

- `GET /health`  
  Simple health check.

---

### Frontend setup and run

From the project root:

```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:5173` by default.

The frontend expects the backend at `VITE_API_BASE_URL` (defaults to `http://localhost:8000`), and uses:

- `POST /generate-quiz` to generate quizzes from the **Generate quiz** tab.
- `GET /quizzes` and `GET /generate-quiz/{id}` from the **History** tab.

---

### Features

- **Tab 1 — Generate Quiz**
  - Validated Wikipedia URL input.
  - Scrapes content (title, summary, sections, article text).
  - Extracts entities using a lightweight heuristic.
  - Sends article data to Gemini via LangChain using prompt templates.
  - Generates 5–10 MCQs (4 options each, correct answer, explanation, difficulty).
  - Generates related topics.
  - Persists article, quiz, and related topics to PostgreSQL.
  - Shows a summary card of the latest quiz and allows entering **take quiz** mode.

- **Tab 2 — History**
  - Displays all previous quizzes in a table.
  - “Details” button opens a modal with the full quiz.

- **Take quiz mode (optional feature)**
  - Step through questions with Previous/Next.
  - Select options, submit quiz, and view score and explanations.

- **Caching**
  - If a URL has already been processed, the backend returns the latest quiz for that article instead of re-scraping and regenerating.

---

### Running in development

1. **Start backend:**

   - Ensure PostgreSQL is running and `.env` is configured.
   - Run `uvicorn app.main:app --reload --port 8000`.

2. **Start frontend:**

   - In `frontend/`, run `npm run dev`.

3. Open the frontend URL (default `http://localhost:5173`) in your browser.

---

### Notes and production considerations

- The entity extraction service is intentionally lightweight and heuristic-based; swap it with spaCy or another NER model for higher accuracy.
- Error handling is implemented in both backend and frontend, but you may harden it further for production (rate limiting, logging, timeouts).
- For production deployment:
  - Use a process manager (e.g. Gunicorn + Uvicorn workers) and a reverse proxy (Nginx).
  - Configure HTTPS and stricter CORS.
  - Move schema evolution to Alembic migrations.

