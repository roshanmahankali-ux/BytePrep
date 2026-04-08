const BookmarkIcon = ({ filled, size = 16 }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path
      d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"
      fill={filled ? 'url(#candyGradient)' : 'none'}
      stroke={filled ? 'url(#candyGradient)' : 'currentColor'}
      strokeWidth="2.5"
    />
  </svg>
)

export default BookmarkIcon