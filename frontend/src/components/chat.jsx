import React, { useState } from 'react'
import API from '../api'

export default function Chat(){
  const [q, setQ] = useState('')
  const [ans, setAns] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const ask = async () => {
    if(!q.trim()) return
    setLoading(true)
    setError(null)
    setAns(null)
    try{
      const res = await API.post('/query', { question: q, top_k: 3 })
      setAns(res.data)
    }catch(err){
      console.error(err)
      setError(err.response?.data?.detail || err.message)
    }finally{
      setLoading(false)
    }
  }

  return (
    <div className="card">
      <h2>Ask about uploaded documents</h2>
      <textarea
        rows="4"
        value={q}
        onChange={e => setQ(e.target.value)}
        placeholder="Type question here..."
      />
      <div style={{display:'flex',gap:8}}>
        <button onClick={ask} disabled={loading}>Ask</button>
        <button onClick={() => { setQ(''); setAns(null); setError(null) }}>Clear</button>
      </div>

      {loading && <div className="status">Thinking...</div>}
      {error && <div className="error">{error}</div>}

      {ans && (
        <div className="answer">
          <h3>Answer</h3>
          <p>{ans.answer}</p>
          <h4>Score: {ans.score?.toFixed(3)}</h4>
          <h4>Sources</h4>
          <ul>
            {ans.sources?.map(s => (
              <li key={s.chunk_id}>
                <b>{s.doc_id} — {s.chunk_id}</b>
                <div className="source-text">{s.text.slice(0,400)}{s.text.length>400?'...':''}</div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
