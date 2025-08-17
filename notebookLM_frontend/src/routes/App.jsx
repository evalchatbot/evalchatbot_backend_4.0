import { Routes, Route, Navigate, Link } from 'react-router-dom';
import Login from '../features/auth/Login.jsx';
import ChatPage from '../features/chat/ChatPage.jsx';
import IngestPage from '../features/ingest/IngestPage.jsx';
import McqPage from '../features/mcq/McqPage.jsx';
import { useAuthStore } from '../store/auth.js';

function Protected({ children }) {
  const token = useAuthStore(s => s.accessToken);
  return token ? children : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <nav className="border-b bg-white sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 py-3 flex gap-4">
          <Link to="/" className="font-semibold">InsightLM</Link>
          <Link to="/chat" className="text-sm">Chat</Link>
          <Link to="/ingest" className="text-sm">Ingest</Link>
          <Link to="/mcq" className="text-sm">MCQ</Link>
        </div>
      </nav>
      <div className="max-w-6xl mx-auto px-4 py-6">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/chat" element={<Protected><ChatPage /></Protected>} />
          <Route path="/ingest" element={<Protected><IngestPage /></Protected>} />
          <Route path="/mcq" element={<Protected><McqPage /></Protected>} />
          <Route path="/" element={<Navigate to="/chat" replace />} />
        </Routes>
      </div>
    </div>
  );
}
