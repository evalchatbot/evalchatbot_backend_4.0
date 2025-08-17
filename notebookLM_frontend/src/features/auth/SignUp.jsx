// src/features/auth/SignUp.jsx
import { useState } from 'react';
import { supabase } from '../../lib/supabase';
import { Link, useNavigate } from 'react-router-dom';

export default function SignUp() {
  const [displayName, setDisplayName] = useState('');
  const [email, setEmail] = useState('');
  const [pw, setPw] = useState('');
  const [phone, setPhone] = useState(''); // optional
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');
  const [hint, setHint] = useState('');
  const [resent, setResent] = useState(false);
  const navigate = useNavigate();

  async function onSubmit(e) {
    e.preventDefault();
    setErr(''); setHint(''); setBusy(true);
    try {
      const { data, error } = await supabase.auth.signUp({
        email,
        password: pw,
        options: {
          data: {
            full_name: displayName,
            phone: phone || null,
          }
        }
      });

      if (error) {
        console.error('signUp error:', { message: error.message, status: error.status, name: error.name, code: error.code });
        setErr(error.message || 'Sign up failed');

        // Helpful hints for common cases
        if ((error.message || '').toLowerCase().includes('database error')) {
          setHint('Likely a DB trigger/column mismatch in public.users. Check that public.users has a nullable "full_name" column and the signup trigger inserts into it.');
        } else if ((error.message || '').toLowerCase().includes('rate limit')) {
          setHint('Email service may be rate-limited. Try again later or configure SMTP.');
        } else if ((error.message || '').toLowerCase().includes('invalid email')) {
          setHint('Make sure the email is valid and has no spaces.');
        }
        return;
      }

      // If email confirmation is ON, you’ll need to confirm before login.
      navigate('/login');
    } catch (e) {
      console.error('signUp exception:', e);
      setErr('Network or unexpected error during sign up');
    } finally {
      setBusy(false);
    }
  }

  async function onResend() {
    try {
      setErr(''); setHint('');
      const { error } = await supabase.auth.resend({ type: 'signup', email });
      if (error) throw error;
      setResent(true);
    } catch (e) {
      setErr(e.message || 'Could not resend confirmation');
    }
  }

  return (
    <div className="max-w-md mx-auto">
      <h1 className="text-2xl font-semibold mb-4">Create account</h1>
      <form onSubmit={onSubmit} className="space-y-3">
        <input className="w-full border rounded px-3 py-2" placeholder="Display name"
               value={displayName} onChange={e=>setDisplayName(e.target.value)} required />
        <input className="w-full border rounded px-3 py-2" placeholder="Email" type="email"
               value={email} onChange={e=>setEmail(e.target.value)} required />
        <input className="w-full border rounded px-3 py-2" placeholder="Phone (optional)"
               value={phone} onChange={e=>setPhone(e.target.value)} />
        <input className="w-full border rounded px-3 py-2" placeholder="Password" type="password"
               value={pw} onChange={e=>setPw(e.target.value)} required />
        <button disabled={busy} className="w-full bg-black text-white rounded py-2">
          {busy ? 'Creating…' : 'Sign Up'}
        </button>

        {err && <p className="text-sm text-red-600 mt-2">{err}</p>}
        {hint && <p className="text-xs text-amber-700 mt-1">{hint}</p>}

        <div className="flex items-center gap-2 pt-2">
          <button type="button" onClick={onResend} className="text-sm underline">
            Resend confirmation
          </button>
          {resent && <span className="text-xs text-green-600">Sent (check spam)</span>}
        </div>
      </form>

      <p className="text-sm mt-4">
        Already have an account? <Link to="/login" className="underline">Log in</Link>
      </p>
    </div>
  );
}
