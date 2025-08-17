import { useState } from 'react';
import { generateMcq, evaluateMcq } from '../../api/endpoints';
import { useAuthStore } from '../../store/auth';

export default function McqPage() {
  const userId = useAuthStore(s => s.userId);
  const [genre, setGenre] = useState('');
  const [quiz, setQuiz] = useState(null);
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);

  async function onGenerate(){
    const q = await generateMcq({ user_id: userId, genre });
    setQuiz(q); setResult(null); setAnswers({});
  }
  async function onSubmit(){
    const payload = { user_id: userId, quiz_id: quiz.quiz_id, answers: Object.entries(answers).map(([id,v]) => ({ question_id: id, answer: v })) };
    const r = await evaluateMcq(payload);
    setResult(r);
  }

  return (
    <div className="max-w-2xl">
      <h1 className="text-xl font-semibold mb-4">MCQ</h1>
      <div className="flex gap-2 mb-4">
        <input className="border rounded px-3 py-2" placeholder="Genre" value={genre} onChange={e=>setGenre(e.target.value)} />
        <button onClick={onGenerate} className="px-4 py-2 rounded bg-black text-white">Generate</button>
      </div>

      {quiz && (
        <div className="space-y-3">
          {quiz.questions?.map(q => (
            <div key={q.id} className="border rounded p-3">
              <p className="font-medium">{q.text}</p>
              <div className="mt-2 grid gap-1">
                {q.options?.map(opt => (
                  <label key={opt} className="flex items-center gap-2">
                    <input
                      type="radio"
                      name={`q-${q.id}`}
                      value={opt}
                      onChange={()=>setAnswers(a=>({ ...a, [q.id]: opt }))}
                    />
                    <span className="text-sm">{opt}</span>
                  </label>
                ))}
              </div>
            </div>
          ))}
          <button onClick={onSubmit} className="px-4 py-2 rounded bg-black text-white">Submit</button>
        </div>
      )}

      {result && (
        <div className="mt-4 border rounded p-3">
          <p className="font-semibold">Score: {result.score}</p>
          {result.feedback && <p className="text-sm mt-1">{result.feedback}</p>}
        </div>
      )}
    </div>
  );
}
