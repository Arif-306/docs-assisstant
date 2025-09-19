import React, { useState } from 'react'
import API from '../api'

export default function Upload(){
  const [file, setFile] = useState(null)
  const [status, setStatus] = useState('No file selected.')
  const [lastDoc, setLastDoc] = useState(null)

  const handleFile = (e) => {
    setFile(e.target.files[0])
    setStatus('File ready to upload.')
  }

  const upload = async () => {
    if(!file){
      setStatus('Please choose a PDF first.')
      return
    }
    const fd = new FormData()
    fd.append('file', file)
    setStatus('Uploading and ingesting...')
    try{
      const res = await API.post('/upload', fd) // do not set Content-Type so browser sets boundary
      setStatus('Ingested: ' + JSON.stringify(res.data))
      setLastDoc(res.data.doc_id || null)
    }catch(err){
      console.error(err)
      setStatus('Error: ' + (err.response?.data?.detail || err.message))
    }
  }

  return (
    <div className="card">
      <h2>Upload PDF</h2>
      <input type="file" accept=".pdf" onChange={handleFile} />
      <button onClick={upload}>Upload & Ingest</button>
      <div className="status">{status}</div>
      {lastDoc && <div>Last doc id: <b>{lastDoc}</b></div>}
    </div>
  )
}
