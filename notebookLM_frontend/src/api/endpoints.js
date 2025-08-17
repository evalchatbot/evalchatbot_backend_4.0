import { api } from './http';

// AUTH
export const issueToken = (body) => api.post('user/token', { json: body }).json();
export const createSession = (body) => api.post('user/session/create', { json: body }).json();

// CHAT
export const askChat = (body) => api.post('chatbot/ask', { json: body }).json();

// BOOKS
export const getGenres = () => api.get('books/genres').json();
export const getBooksByGenre = (genre) => api.get(`books/${encodeURIComponent(genre)}`).json();

// INGEST
export const uploadBook = (formData) => api.post('ingest/upload', { body: formData }).json();

// MCQ
export const generateMcq = (body) => api.post('mcq/generate', { json: body }).json();
export const evaluateMcq = (body) => api.post('mcq/evaluate', { json: body }).json();
