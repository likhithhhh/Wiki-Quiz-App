import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
});

export const generateQuiz = async (url) => {
  const response = await apiClient.post("/generate-quiz", { url });
  return response.data;
};

export const fetchQuizzes = async () => {
  const response = await apiClient.get("/quizzes");
  return response.data;
};

export const fetchQuizDetail = async (id) => {
  const response = await apiClient.get(`/generate-quiz/${id}`);
  return response.data;
};

