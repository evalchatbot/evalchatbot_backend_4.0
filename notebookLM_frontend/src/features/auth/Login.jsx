import { useState } from 'react';
import { issueToken, createSession } from '../../api/endpoints';
import { useAuthStore } from '../../store/auth';
import { useNavigate } from 'react-router-dom';

export default function Login() {
  const [userId, setUserId] = useState('');
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');
  const setAuth = useAuthStore(s => s.setAuth);
  const setSessionId = useAuthStore(s => s.setSessionId);
  const navigate = useNavigate();

  async function onSubmit(e) {
    e.preventDefault();
    setErr('');
    setBusy(true);
    try {
      const tokenRes = await issueToken({ user_id: userId });
      setAuth({ userId, accessToken: tokenRes.access_token });
      const sessionRes = await createSession({ user_id: userId });
      setSessionId(sessionRes.session_id);
      navigate('/chat');
    } catch (e) {
      console.error(e);
      setErr('Login failed. Check server and user_id.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="max-w-md mx-auto">
      <h1 className="text-2xl font-semibold mb-4">Sign In</h1>
      <form onSubmit={onSubmit} className="space-y-3">
        <input
          className="w-full border rounded px-3 py-2"
          placeholder="Enter user_id"
          value={userId}
          onChange={(e)=>setUserId(e.target.value)}
          required
        />
        <button disabled={busy} className="w-full bg-black text-white rounded py-2">
          {busy ? 'Signing in…' : 'Sign In'}
        </button>
        {err && <p className="text-sm text-red-600">{err}</p>}
      </form>
    </div>
  );
}
