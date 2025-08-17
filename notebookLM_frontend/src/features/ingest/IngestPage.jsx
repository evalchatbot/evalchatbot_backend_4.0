import { useState } from 'react';
import { uploadBook } from '../../api/endpoints';

export default function IngestPage() {
  const [title, setTitle] = useState('');
  const [genre, setGenre] = useState('');
  const [author, setAuthor] = useState('');
  const [file, setFile] = useState(null);
  const [msg, setMsg] = useState('');

  async function onSubmit(e){
    e.preventDefault();
    const fd = new FormData();
    if (file) fd.append('file', file);
    fd.append('title', title);
    if (author) fd.append('author', author);
    if (genre) fd.append('genre', genre);
    const res = await uploadBook(fd);
    setMsg(`Uploaded. Chunks: ${res.num_chunks ?? 'n/a'}`);
  }

  return (
    <div className="max-w-md">
      <h1 className="text-xl font-semibold mb-4">Upload Book (Admin)</h1>
      <form onSubmit={onSubmit} className="space-y-2">
        <input className="w-full border rounded px-3 py-2" placeholder="Title" value={title} onChange={e=>setTitle(e.target.value)} required />
        <input className="w-full border rounded px-3 py-2" placeholder="Author (optional)" value={author} onChange={e=>setAuthor(e.target.value)} />
        <input className="w-full border rounded px-3 py-2" placeholder="Genre" value={genre} onChange={e=>setGenre(e.target.value)} required />
        <input type="file" onChange={e=>setFile(e.target.files?.[0] || null)} required />
        <button className="w-full bg-black text-white rounded py-2">Upload</button>
      </form>
      {msg && <p className="mt-3 text-sm">{msg}</p>}
    </div>
  );
}
