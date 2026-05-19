import BookmarkIcon from './BookmarkIcon'
const DIFFICULTIES = ['All', 'Easy', 'Medium', 'Hard']

const FilterBar = ({ selected, onSelect, showFavourites, onToggleFavourites, onReset }) => {
  return (
    <div className="filter-bar">
      <div className="filter-buttons">
        {DIFFICULTIES.map(level => (
          <button
            key={level}
            className={`filter-btn ${selected === level ? 'active' : ''} ${level.toLowerCase()}`}
            onClick={() => onSelect(level)}
          >
            {level}
          </button>
        ))}

        {/* Favourites toggle */}
        <button
          className={`filter-btn favourite-btn ${showFavourites ? 'active' : ''}`}
          onClick={onToggleFavourites}
        >
          <BookmarkIcon filled={showFavourites} size={14} />
          Favourites
        </button>
      </div>

      <button className="reset-btn" onClick={onReset}>
        ⇄ Reset Deck
      </button>
    </div>
  )
}

export default FilterBar