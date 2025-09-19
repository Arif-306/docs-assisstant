import React from 'react'
import Upload from './components/Upload.jsx'
import Chat from './components/Chat.jsx'

export default function App(){
  return (
    <div className="container">
      <header>
        <h1>AlphaDoc Assistant</h1>
        <p>Upload a PDF → Ask questions about it.</p>
      </header>

      <main>
        <section className="left">
          <Upload />
        </section>

        <section className="right">
          <Chat />
        </section>
      </main>

      <footer>
        <small>Run backend on <code>http://localhost:8000</code> before using.</small>
      </footer>
    </div>
  )
}
