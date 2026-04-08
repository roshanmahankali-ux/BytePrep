import FlashcardDeck from './components/FlashcardDeck'
import './App.css'

function App() {
  return (
    <div className="app">
       {/* Global SVG gradient — referenced by all BookmarkIcons */}
      <svg width="0" height="0" style={{ position: 'absolute' }}>
        <defs>
          <linearGradient id="candyGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#ec4899" />
            <stop offset="100%" stopColor="#8b5cf6" />
          </linearGradient>
        </defs>
      </svg>
      
      <header className="app-header">
        <h1>⚡ BytePrep - System Design Flashcards</h1>
        <p>Master system design concepts one card at a time at your finger tips</p>
      </header>
      <main>
        <FlashcardDeck />
      </main>
    </div>
  )
}

export default App