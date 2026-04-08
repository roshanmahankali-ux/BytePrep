import axios from 'axios'

const BASE_URL = 'http://localhost:8000/api/flashcards'

// READ — filter by difficulty and/or favourite
export const getFlashcards = async (difficulty = null, favourite = null) => {
  const params = {}
  if (difficulty) params.difficulty = difficulty
  if (favourite !== null) params.favourite = favourite
  const res = await axios.get(BASE_URL, { params })
  return res.data
}

// READ - get single card
export const getFlashcard = async (id) => {
  const res = await axios.get(`${BASE_URL}/${id}`)
  return res.data
}

// CREATE - add a new card
export const createFlashcard = async (cardData) => {
  const res = await axios.post(BASE_URL, cardData)
  return res.data
}

// UPDATE - edit an existing card
export const updateFlashcard = async (id, cardData) => {
  const res = await axios.put(`${BASE_URL}/${id}`, cardData)
  return res.data
}

// DELETE - remove a card
export const deleteFlashcard = async (id) => {
  await axios.delete(`${BASE_URL}/${id}`)
}