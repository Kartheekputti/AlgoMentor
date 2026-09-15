import { useState, useMemo } from 'react'
import {
  ExternalLink,
  ChevronDown,
  ChevronUp,
  Search,
  MessageSquare
} from 'lucide-react'
import confetti from 'canvas-confetti'

const STRIVER_AZ_URL = 'https://takeuforward.org/dsa/strivers-a2z-sheet-learn-dsa-a-to-z'

export default function DSASheet({
  sheetProgress,
  onToggleProblem,
  onAskAIAboutProblem,
  _loggedUser
}) {
  const [activePhase, setActivePhase] = useState('all') // 'all' | 'phase-1' | 'phase-2' | 'phase-3'
  const [searchQuery, setSearchQuery] = useState('')
  const [expandedTopics, setExpandedTopics] = useState({ Arrays: true, Hashing: true })

  const totalDone = useMemo(
    () => sheetProgress.reduce((sum, topic) => sum + (topic.solved?.filter(Boolean).length ?? topic.done ?? 0), 0),
    [sheetProgress]
  )

  const totalQuestions = useMemo(
    () => sheetProgress.reduce((sum, topic) => sum + (topic.problems?.length ?? topic.total ?? 0), 0),
    [sheetProgress]
  )

  const completionPercent = totalQuestions ? Math.round((totalDone / totalQuestions) * 100) : 0

  const toggleTopicExpand = (topicName) => {
    setExpandedTopics((prev) => ({
      ...prev,
      [topicName]: !prev[topicName],
    }))
  }

  const handleCheckboxChange = (topicIdx, problemIdx, isAlreadySolved) => {
    onToggleProblem(topicIdx, problemIdx)
    if (!isAlreadySolved) {
      // Trigger confetti celebration
      try {
        confetti({
          particleCount: 50,
          spread: 60,
          origin: { y: 0.8 },
          colors: ['#6366f1', '#8b5cf6', '#10b981', '#38bdf8'],
        })
      } catch (_err) {
        // ignore
      }
    }
  }

  // Phases partitioning
  const phases = [
    { id: 'phase-1', label: 'Phase 1: Foundation', range: [0, 6] },
    { id: 'phase-2', label: 'Phase 2: Intermediate', range: [6, 12] },
    { id: 'phase-3', label: 'Phase 3: Advanced', range: [12, sheetProgress.length] },
  ]

  const filteredTopics = sheetProgress.map((topic, originalIdx) => ({
    ...topic,
    originalIdx,
  })).filter((topic) => {
    // Phase check
    if (activePhase !== 'all') {
      const activeP = phases.find((p) => p.id === activePhase)
      if (activeP) {
        const [start, end] = activeP.range
        if (topic.originalIdx < start || topic.originalIdx >= end) return false
      }
    }

    // Search query check
    if (!searchQuery) return true
    const q = searchQuery.toLowerCase()
    const matchesTopic = topic.name.toLowerCase().includes(q)
    const matchesProblem = topic.problems?.some((p) => p.toLowerCase().includes(q))
    return matchesTopic || matchesProblem
  })

  return (
    <div className="sheet-container">
      {/* Top Banner & Stats */}
      <div className="sheet-hero-card">
        <div className="sheet-hero-left">
          <div className="sheet-badge-row">
            <span className="sheet-badge-primary">TakeUForward Striver A-Z</span>
            <span className="sheet-badge-secondary">Comprehensive DSA Track</span>
          </div>
          <h2 className="sheet-hero-title">Striver’s A-to-Z DSA Sheet</h2>
          <p className="sheet-hero-desc">
            Master all core data structures, algorithms, and technical interview patterns systematically.
            Check off solved problems, track your streak, and ask AlgoMentor AI for instant explanations.
          </p>

          <div className="sheet-hero-actions">
            <a
              href={STRIVER_AZ_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="sheet-external-btn"
            >
              <span>Open TakeUForward Official Sheet</span>
              <ExternalLink size={15} />
            </a>
          </div>
        </div>

        <div className="sheet-hero-right">
          <div className="sheet-progress-gauge">
            <div className="gauge-number">{completionPercent}%</div>
            <div className="gauge-label">Completed</div>
          </div>
          <div className="gauge-meta">
            <div className="gauge-stat">
              <strong>{totalDone}</strong>
              <span>Solved</span>
            </div>
            <div className="gauge-stat-divider" />
            <div className="gauge-stat">
              <strong>{totalQuestions}</strong>
              <span>Total Problems</span>
            </div>
          </div>
          <div className="sheet-progress-bar-wrap">
            <div
              className="sheet-progress-bar-fill"
              style={{ width: `${completionPercent}%` }}
            />
          </div>
        </div>
      </div>

      {/* Filter and Phase Navigation */}
      <div className="sheet-controls-bar">
        <div className="sheet-phase-pills">
          <button
            type="button"
            className={`phase-pill ${activePhase === 'all' ? 'active' : ''}`}
            onClick={() => setActivePhase('all')}
          >
            All Topics ({sheetProgress.length})
          </button>
          {phases.map((p) => (
            <button
              key={p.id}
              type="button"
              className={`phase-pill ${activePhase === p.id ? 'active' : ''}`}
              onClick={() => setActivePhase(p.id)}
            >
              {p.label}
            </button>
          ))}
        </div>

        <div className="sheet-search-wrap">
          <Search size={15} className="text-slate-400" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Filter topics or problem names..."
          />
        </div>
      </div>

      {/* Topics Accordion Grid */}
      <div className="sheet-topics-grid">
        {filteredTopics.map((topic) => {
          const isExpanded = Boolean(expandedTopics[topic.name])
          const doneCount = topic.solved?.filter(Boolean).length ?? topic.done ?? 0
          const totalCount = topic.problems?.length ?? topic.total ?? 0
          const topicPercent = totalCount ? Math.round((doneCount / totalCount) * 100) : 0
          const isCompleted = doneCount === totalCount && totalCount > 0

          return (
            <div key={topic.name} className={`sheet-topic-card ${isCompleted ? 'completed' : ''}`}>
              <div
                className="sheet-topic-header"
                onClick={() => toggleTopicExpand(topic.name)}
              >
                <div className="topic-header-left">
                  <div className={`topic-index-badge ${isCompleted ? 'done' : ''}`}>
                    {topic.originalIdx + 1}
                  </div>
                  <div>
                    <h3 className="topic-name">{topic.name}</h3>
                    <span className="topic-subtext">
                      {doneCount} of {totalCount} solved ({topicPercent}%)
                    </span>
                  </div>
                </div>

                <div className="topic-header-right">
                  <div className="topic-mini-progress">
                    <div
                      className="topic-mini-progress-fill"
                      style={{ width: `${topicPercent}%` }}
                    />
                  </div>
                  <button type="button" className="topic-expand-btn">
                    {isExpanded ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
                  </button>
                </div>
              </div>

              {/* Problems List */}
              {isExpanded && (
                <div className="sheet-problems-list">
                  {topic.problems.map((probName, probIdx) => {
                    const isSolved = Boolean(topic.solved?.[probIdx])
                    return (
                      <div
                        key={probIdx}
                        className={`problem-item-row ${isSolved ? 'solved' : ''}`}
                      >
                        <label className="problem-label">
                          <input
                            type="checkbox"
                            checked={isSolved}
                            onChange={() =>
                              handleCheckboxChange(topic.originalIdx, probIdx, isSolved)
                            }
                            className="problem-checkbox"
                          />
                          <span className="problem-title">{probName}</span>
                        </label>

                        <div className="problem-actions">
                          <button
                            type="button"
                            className="ask-ai-problem-btn"
                            title={`Ask AlgoMentor AI for an explanation of ${probName}`}
                            onClick={() => onAskAIAboutProblem && onAskAIAboutProblem(probName)}
                          >
                            <MessageSquare size={13} />
                            <span>Ask AI</span>
                          </button>
                        </div>
                      </div>
                    )
                  })}
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
