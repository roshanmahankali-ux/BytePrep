import { useState, useEffect } from 'react'
import { getFlashcards, createFlashcard, updateFlashcard, deleteFlashcard } from '../services/api'

export const useFlashcards = (difficulty, onlyFavourites) => {
  const [cards, setCards] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [searchQuery, setSearchQuery] = useState('')

  // Fetch cards whenever difficulty filter changes
  useEffect(() => {
    fetchCards()
  }, [difficulty, onlyFavourites])

  const fetchCards = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await getFlashcards(
        difficulty,
        onlyFavourites ? true : null
      )
      setCards(data)
    } catch (err) {
      setError('Failed to load flashcards. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  const addCard = async (cardData) => {
    const newCard = await createFlashcard(cardData)
    setCards(prev => [...prev, newCard])
  }

  const editCard = async (id, cardData) => {
    const updated = await updateFlashcard(id, cardData)
    setCards(prev => prev.map(c => c.id === id ? updated : c))
  }

  const removeCard = async (id) => {
    await deleteFlashcard(id)
    setCards(prev => prev.filter(c => c.id !== id))
  }

  // Toggle favourite on/off
  const toggleFavourite = async (id, current) => {
    const updated = await updateFlashcard(id, { favourite: !current })
    setCards(prev => prev.map(c => c.id === id ? updated : c))
  }

  const resetDeck = () => fetchCards()

  const filteredCards = cards.filter(c => {
    if (!searchQuery.trim()) return true
    const q = searchQuery.toLowerCase()
    return c.question.toLowerCase().includes(q) || c.answer.toLowerCase().includes(q)
  })

  return { cards: filteredCards, loading, error, addCard, editCard, removeCard, toggleFavourite, resetDeck, searchQuery,
  setSearchQuery }
}