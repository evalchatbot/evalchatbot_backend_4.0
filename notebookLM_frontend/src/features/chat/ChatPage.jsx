import { useState } from 'react';
import { useAuthStore } from '../../store/auth';
import { askChat, getGenres } from '../../api/endpoints';
import { useQuery } from '@tanstack/react-query';
import ReactMarkdown from 'react-markdown';

export default function ChatPage() {
  const userId = useAuthStore(s => s.userId);
  const sessionId = useAuthStore(s => s.sessionId);
  const [genre, setGenre] = useState('');
  const [q, setQ] = useState('');
  const [reply, setReply] = useState(null);
  const [busy, setBusy] = useState(false);

  const { data: genres } = useQuery({
    queryKey: ['genres'],
    queryFn: getGenres
  });

  async function onAsk(e) {
    e.preventDefault();
    setBusy(true);
    setReply(null);
    try {
      const res = await askChat({ user_id: userId, session_id: sessionId, question: q, genre });
      setReply(res);
    } catch (e) {
      console.error(e);
      setReply({ answer: 'Error: request failed.' });
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="grid md:grid-cols-[240px_1fr] gap-6">
      <aside className="space-y-2">
        <h2 className="font-medium">Genres</h2>
        <div className="flex flex-col gap-1">
          {(genres?.genres || []).map(g => (
            <button
              key={g}
              onClick={()=>setGenre(g)}
              className={`text-left px-3 py-2 rounded border ${genre===g ? 'bg-black text-white' : 'bg-white'}`}
            >{g}</button>
          ))}
        </div>
      </aside>

      <main>
        <form onSubmit={onAsk} className="flex gap-2 mb-4">
          <input
            className="flex-1 border rounded px-3 py-2"
            placeholder="Ask a question…"
            value={q}
            onChange={e=>setQ(e.target.value)}
          />
          <button disabled={!q || !genre || busy} className="px-4 py-2 rounded bg-black text-white">
            {busy ? 'Asking…' : 'Ask'}
          </button>
        </form>

        {reply && (
          <div className="space-y-4">
            <div className="prose max-w-none">
              <ReactMarkdown>{reply.answer || ''}</ReactMarkdown>
            </div>

            {Array.isArray(reply.sources) && reply.sources.length > 0 && (
              <div>
                <h3 className="font-semibold mb-1">Sources</h3>
                <ul className="list-disc ml-6">
                  {reply.sources.map((s, i) => (
                    <li key={i}><span className="text-sm">{JSON.stringify(s)}</span></li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
