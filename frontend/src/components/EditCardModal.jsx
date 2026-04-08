import { useState } from 'react'

const CATEGORIES = ['Fundamentals', 'Scalability', 'Databases', 'Networking', 'Architecture', 'Performance', 'Security', 'Infrastructure', 'System Design']
const DIFFICULTIES = ['Easy', 'Medium', 'Hard']

const EditCardModal = ({ card, onClose, onEdit }) => {
  const [form, setForm] = useState({
    question: card.question,
    answer: card.answer,
    category: card.category,
    difficulty: card.difficulty
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
      await onEdit(card.id, form)
      onClose()
    } catch {
      setError('Failed to update card. Try again.')
    }
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <h2>Edit Flashcard</h2>
        {error && <p className="form-error">{error}</p>}
        <form onSubmit={handleSubmit}>
          <label>Question
            <textarea
              name="question"
              value={form.question}
              onChange={handleChange}
              rows={3}
            />
          </label>
          <label>Answer
            <textarea
              name="answer"
              value={form.answer}
              onChange={handleChange}
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
            <button type="submit" className="submit-btn">Save Changes</button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default EditCardModal