import { useState } from 'react'
import BookmarkIcon from './BookmarkIcon'

const CATEGORIES = ['Fundamentals', 'Scalability', 'Databases', 'Networking', 'Architecture', 'Performance', 'Security', 'Infrastructure', 'System Design']
const DIFFICULTIES = ['Easy', 'Medium', 'Hard']

const AddCardModal = ({ onClose, onAdd }) => {
  const [form, setForm] = useState({
    question: '',
    answer: '',
    category: 'Fundamentals',
    difficulty: 'Easy',
    favourite: false
  })
  const [error, setError] = useState('')

  const handleChange = (e) => {
    setForm(prev => ({ ...prev, [e.target.name]: e.target.value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!form.question.trim() || !form.answer.trim()) {
      setError('Question and answer are required.')
      return
    }
    try {
      await onAdd(form)
      onClose()
    } catch {
      setError('Failed to add card. Try again.')
    }
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <div className="modal-title-row">
          <h2>Add New Flashcard</h2>
          {/* Bookmark toggle in header */}
          <button
            type="button"
            className={`modal-bookmark ${form.favourite ? 'bookmarked' : ''}`}
            onClick={() => setForm(prev => ({ ...prev, favourite: !prev.favourite }))}
            title={form.favourite ? 'Remove from favourites' : 'Mark as favourite'}
          >
          <BookmarkIcon filled={form.favourite} size={18} />
          </button>
        </div>

        {error && <p className="form-error">{error}</p>}

        <form onSubmit={handleSubmit}>
          <label>Question
            <textarea
              name="question"
              value={form.question}
              onChange={handleChange}
              placeholder="e.g. What is consistent hashing?"
              rows={3}
            />
          </label>
          <label>Answer
            <textarea
              name="answer"
              value={form.answer}
              onChange={handleChange}
              placeholder="e.g. A technique to distribute data..."
              rows={4}
            />
          </label>
          <div className="form-row">
            <label>Category
              <select name="category" value={form.category} onChange={handleChange}>
                {CATEGORIES.map(c => <option key={c}>{c}</option>)}
              </select>
            </label>
            <label>Difficulty
              <select name="difficulty" value={form.difficulty} onChange={handleChange}>
                {DIFFICULTIES.map(d => <option key={d}>{d}</option>)}
              </select>
            </label>
          </div>
          <div className="modal-actions">
            <button type="button" className="cancel-btn" onClick={onClose}>Cancel</button>
            <button type="submit" className="submit-btn">Add Card</button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default AddCardModal