import { useState } from 'react'
import './App.css'

function App() {
  const [proteinText, setProteinText] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [result, setResult] = useState(null)

  async function handleSubmit(e) {
    e.preventDefault()
    if (!proteinText.trim()) return
    setIsSubmitting(true)
    setResult(null)
    
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'https://amp-classifier.onrender.com'
      const response = await fetch(`${apiUrl}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ seq: proteinText.trim() }),
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      if (data.results && data.results.length > 0) {
        const result = data.results[0]
        setResult({
          label: result.prediction,
          confidence: result.confidence ? (result.confidence * 100).toFixed(1) : null,
          cleaned: result.cleaned,
        })
      } else {
        throw new Error('No results returned from API')
      }
    } catch (error) {
      setResult({
        label: 'Error',
        confidence: null,
        error: error.message,
      })
    } finally {
      setIsSubmitting(false)
    }
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
              {result.error ? (
                <div className="error">Error: {result.error}</div>
              ) : (
                <>
                  <div className="prediction">Result: {result.label}</div>
                  {result.confidence && (
                    <div className="confidence">Confidence: {result.confidence}%</div>
                  )}
                  {result.cleaned && result.cleaned !== proteinText.trim() && (
                    <div className="cleaned">Cleaned sequence: {result.cleaned}</div>
                  )}
                </>
              )}
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
