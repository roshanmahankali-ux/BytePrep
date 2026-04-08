const ProgressBar = ({ total, remaining }) => {
  const completed = total - remaining
  const percentage = total === 0 ? 0 : (completed / total) * 100

  return (
    <div className="progress-container">
      <div className="progress-info">
        <span>{completed} reviewed</span>
        <span>{remaining} remaining</span>
      </div>
      <div className="progress-track">
        <div
          className="progress-fill"
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  )
}

export default ProgressBar