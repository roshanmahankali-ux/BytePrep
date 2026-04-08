import { useState } from 'react'
import BookmarkIcon from './BookmarkIcon'

const FlashcardCard = ({ card, onDismiss, onDelete, onEdit, onToggleFavourite }) => {
  const [flipped, setFlipped] = useState(false)
  const [leaving, setLeaving] = useState(false)

  const handleFlip = () => {
    if (!flipped) setFlipped(true)
  }

  const handleNext = (e) => {
    e.stopPropagation()
    setLeaving(true)
    setTimeout(() => onDismiss(), 400)
  }

  return (
    <div
      className={`card-wrapper ${flipped ? 'flipped' : ''} ${leaving ? 'leaving' : ''}`}
      onClick={handleFlip}
    >
      <div className="card-inner">
        {/* Front */}
        <div className="card-front">
          <div className="card-top">
            <span className={`difficulty-badge ${card.difficulty.toLowerCase()}`}>
              {card.difficulty}
            </span>
            <span className="category-label">{card.category}</span>
          </div>
          <p className="card-question">{card.question}</p>
          <span className="flip-hint">✨ Click to reveal answer</span>
        </div>

        {/* Back */}
        <div className="card-back">
          <div className="card-top">
            <span className={`difficulty-badge ${card.difficulty.toLowerCase()}`}>
              {card.difficulty}
            </span>
          </div>
          <p className="card-answer">{card.answer}</p>
          <button className="next-btn" onClick={handleNext}>
            Next Card →
          </button>
        </div>
      </div>

      {/* Bookmark + Edit + Delete */}
      <div className="card-actions" onClick={e => e.stopPropagation()}>
        <button
          className={`bookmark-btn ${card.favourite ? 'bookmarked' : ''}`}
          onClick={() => onToggleFavourite(card.id, card.favourite)}
          title={card.favourite ? 'Remove from favourites' : 'Add to favourites'}
        >
          <BookmarkIcon filled={card.favourite} size={14} />
        </button>
        <button className="edit-btn" onClick={() => onEdit(card)} title="Edit card">✏️</button>
        <button className="delete-btn" onClick={() => onDelete(card.id)} title="Delete card">🗑️</button>
      </div>
    </div>
  )
}

export default FlashcardCard