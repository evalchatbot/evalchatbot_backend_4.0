import { Link } from 'react-router-dom';
import { useAuthStore } from '../../store/auth';

export default function Home() {
  const token = useAuthStore(s => s.accessToken);

  return (
    <div className="max-w-3xl mx-auto">
      <h1 className="text-3xl md:text-4xl font-bold mb-3">Welcome to InsightLM</h1>
      <p className="text-gray-700 mb-6">
        Chat with your books, upload new content, and test yourself with MCQs — all in one place.
      </p>

      {!token ? (
        <div className="flex gap-3">
          <Link to="/signup" className="px-4 py-2 rounded bg-black text-white">
            Create an account
          </Link>
          <Link to="/login" className="px-4 py-2 rounded border">
            Log in
          </Link>
        </div>
      ) : (
        <div className="flex gap-3">
          <Link to="/chat" className="px-4 py-2 rounded bg-black text-white">
            Go to Chat
          </Link>
          <Link to="/ingest" className="px-4 py-2 rounded border">
            Upload a Book
          </Link>
          <Link to="/mcq" className="px-4 py-2 rounded border">
            Take an MCQ
          </Link>
        </div>
      )}
    </div>
  );
}
