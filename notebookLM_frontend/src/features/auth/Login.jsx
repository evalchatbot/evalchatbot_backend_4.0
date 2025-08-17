import { useState } from 'react';
import { supabase } from '../../lib/supabase';
import { useAuthStore } from '../../store/auth';
import { createSession } from '../../api/endpoints';
import { useNavigate, Link } from 'react-router-dom';

export default function Login() {
  const [email, setEmail] = useState('');
  const [pw, setPw] = useState('');
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');
  const setSessionId = useAuthStore(s => s.setSessionId);
  const navigate = useNavigate();

  async function onSubmit(e) {
    e.preventDefault();
    setErr(''); setBusy(true);
    console.log('email:', email, 'pw length:', pw.length);

    try {
      const { data, error } = await supabase.auth.signInWithPassword({ email, password: pw });
      if (error) throw error;

      // create a server-side session for this user (no body)
      const res = await createSession();
      setSessionId(res.session_id);

      navigate('/chat');
    } catch (e) {
      setErr(e.message || 'Login failed');
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="max-w-md mx-auto">
      <h1 className="text-2xl font-semibold mb-4">Log in</h1>
      <form onSubmit={onSubmit} className="space-y-3">
        <input className="w-full border rounded px-3 py-2" placeholder="Email"
               value={email} onChange={e=>setEmail(e.target.value)} type="email" required />
        <input className="w-full border rounded px-3 py-2" placeholder="Password"
               value={pw} onChange={e=>setPw(e.target.value)} type="password" required />
        <button disabled={busy} className="w-full bg-black text-white rounded py-2">
          {busy ? 'Signing in…' : 'Sign In'}
        </button>
        {err && <p className="text-sm text-red-600">{err}</p>}
      </form>
      <p className="text-sm mt-2">No account? <Link to="/signup" className="underline">Sign up</Link></p>
    </div>
  );
}
