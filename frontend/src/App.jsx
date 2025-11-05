import { useState } from 'react'
import './App.css'

function App() {
  const [proteinText, setProteinText] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [result, setResult] = useState(null)

  function handleSubmit(e) {
    e.preventDefault()
    if (!proteinText.trim()) return
    setIsSubmitting(true)
    // Placeholder inference; replace with real backend call later
    // Simulate a short delay for UX
    setTimeout(() => {
      setResult({ label: 'AMP', confidence: 98.0 })
      setIsSubmitting(false)
    }, 400)
  }

  return (
    <div className="page">
      <main className="card">
        <section className="visual" aria-hidden="true">
          {/* Placeholder for hero image. Keep background black per request. */}
        </section>

        <section className="content">
          <div className="brand">▣</div>
          <h1 className="title">AMP Classifier</h1>
          <p className="tagline">
            enter the protein and get classified whether its amp or non-amp
          </p>

          <form className="chat" onSubmit={handleSubmit}>
            <label htmlFor="protein-input" className="sr-only">send a message</label>
            <input
              id="protein-input"
              className="input"
              type="text"
              placeholder="send a message — paste protein sequence here"
              value={proteinText}
              onChange={(e) => setProteinText(e.target.value)}
              disabled={isSubmitting}
            />
            <button className="send" type="submit" disabled={isSubmitting}>
              {isSubmitting ? '...' : 'Send'}
            </button>
          </form>

          {result && (
            <div className="result" role="status">
              result: {result.label}, Confidence: {result.confidence}
            </div>
          )}

          <div className="footer-links">
            <span>web</span>
            <span>•</span>
            <span>product</span>
            <span>•</span>
            <span>brand</span>
          </div>
        </section>
      </main>
    </div>
  )
}

export default App
