import { useState } from 'react'
import { useFlashcards } from '../hooks/useFlashcards'
import FlashcardCard from './FlashcardCard'
import FilterBar from './FilterBar'
import AddCardModal from './AddCardModal'
import EditCardModal from './EditCardModal'
import { recordReview } from '../services/api'

const FlashcardDeck = () => {
  const [difficulty, setDifficulty] = useState('All')
  const [showFavourites, setShowFavourites] = useState(false)
  const [showAdd, setShowAdd] = useState(false)
  const [editingCard, setEditingCard] = useState(null)
  const [currentIndex, setCurrentIndex] = useState(0)

  const activeFilter = difficulty === 'All' ? null : difficulty
  const { cards, loading, error, addCard, editCard, removeCard, toggleFavourite, resetDeck } =
    useFlashcards(activeFilter, showFavourites)

  const handleDismiss = async () => {
  if (currentCard) {
    try {
      await recordReview(currentCard.id)
    } catch (err) {
      console.log("Error saving user History")
    }
  }
  setCurrentIndex(prev => prev + 1)
}

  const handleReset = () => {
    resetDeck()
    setCurrentIndex(0)
  }

  const handleEdit = async (id, cardData) => {
  await editCard(id, cardData)
  handleReset()
}

  const handleFilterChange = (level) => {
    setDifficulty(level)
    setCurrentIndex(0)
  }

  const handleToggleFavourites = () => {
    setShowFavourites(prev => !prev)
    setCurrentIndex(0)
  }

  const currentCard = cards[currentIndex]
  const remaining = cards.length - currentIndex
  const completed = currentIndex
  const percentage = cards.length === 0 ? 0 : (completed / cards.length) * 100

  if (loading) return (
    <div className="loading-state">
      <div className="spinner" />
      <p>Loading flashcards...</p>
    </div>
  )

  if (error) return (
    <div className="error-state">
      <p>⚠️ {error}</p>
      <button onClick={resetDeck}>Try Again</button>
    </div>
  )

  return (
    <div className="deck-container">
      <FilterBar
        selected={difficulty}
        onSelect={handleFilterChange}
        showFavourites={showFavourites}
        onToggleFavourites={handleToggleFavourites}
        onReset={handleReset}
      />

      <div className="progress-container">
        <div className="progress-info">
          <span>{completed} reviewed</span>
          <span>{remaining} remaining</span>
        </div>
        <div className="progress-track">
          <div className="progress-fill" style={{ width: `${percentage}%` }} />
        </div>
      </div>

      <div className="deck-header">
        <p className="card-count">
          {cards.length > 0
            ? `Card ${Math.min(currentIndex + 1, cards.length)} of ${cards.length}`
            : ''}
        </p>
        <button className="add-btn" onClick={() => setShowAdd(true)}>+ Add Card</button>
      </div>

      <div className="single-card-view">
        {!currentCard ? (
          <div className="empty-state">
            {cards.length === 0
              ? <><p>No cards found.</p><p>Try a different filter or add new cards!</p></>
              : <><p>Hoorayyyy! All Done 💃🥳 </p><p>Great work. Wanna start reviewing again?</p></>
            }
            <button className="reset-cta" onClick={handleReset}>🔄 Reset Deck</button>
          </div>
        ) : (
          <FlashcardCard
            key={currentCard.id}
            card={currentCard}
            onDismiss={handleDismiss}
            onDelete={async (id) => { await removeCard(id); setCurrentIndex(0) }}
            onEdit={setEditingCard}
            onToggleFavourite={toggleFavourite}
          />
        )}
      </div>

      {showAdd && <AddCardModal onClose={() => setShowAdd(false)} onAdd={addCard} />}
      {editingCard && (
        <EditCardModal
          card={editingCard}
          onClose={() => setEditingCard(null)}
          onEdit={handleEdit}
        />
      )}
    </div>
  )
}

export default FlashcardDeck