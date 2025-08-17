import { Routes, Route, Navigate, Link, useNavigate } from 'react-router-dom';
import Login from '../features/auth/Login.jsx';
import SignUp from '../features/auth/SignUp.jsx';
import ChatPage from '../features/chat/ChatPage.jsx';
import IngestPage from '../features/ingest/IngestPage.jsx';
import McqPage from '../features/mcq/McqPage.jsx';
import Home from '../features/home/Home.jsx';
import { useAuthStore } from '../store/auth';

function Protected({ children }) {
  const token = useAuthStore(s => s.accessToken);
  return token ? children : <Navigate to="/login" replace />;
}

export default function App() {
  const navigate = useNavigate();
  const token = useAuthStore(s => s.accessToken);
  const user = useAuthStore(s => s.user);
  const logout = useAuthStore(s => s.logout);

  async function onLogout() {
    await logout();
    navigate('/');
  }

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <nav className="border-b bg-white sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center gap-4">
          <Link to="/" className="font-semibold">InsightLM</Link>

          <div className="flex items-center gap-3">
            <Link to="/chat" className="text-sm hover:underline">Chat</Link>
            <Link to="/ingest" className="text-sm hover:underline">Ingest</Link>
            <Link to="/mcq" className="text-sm hover:underline">MCQ</Link>
          </div>

          <div className="ml-auto flex items-center gap-3">
            {!token ? (
              <>
                <Link to="/login" className="text-sm px-3 py-1.5 rounded border hover:bg-gray-50">
                  Log in
                </Link>
                <Link to="/signup" className="text-sm px-3 py-1.5 rounded bg-black text-white">
                  Sign up
                </Link>
              </>
            ) : (
              <>
                <span className="text-sm text-gray-700">
                  {user?.email ?? 'Account'}
                </span>
                <button
                  onClick={onLogout}
                  className="text-sm px-3 py-1.5 rounded border hover:bg-gray-50"
                >
                  Log out
                </button>
              </>
            )}
          </div>
        </div>
      </nav>

      <div className="max-w-6xl mx-auto px-4 py-6">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />

          <Route path="/chat" element={<Protected><ChatPage /></Protected>} />
          <Route path="/ingest" element={<Protected><IngestPage /></Protected>} />
          <Route path="/mcq" element={<Protected><McqPage /></Protected>} />

          {/* fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </div>
  );
}
