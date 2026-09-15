import { useEffect, useMemo, useRef, useState } from 'react'
import './App.css'
import AIChat from './components/AIChat'
import SamsungNotes from './components/SamsungNotes'
import DSASheet from './components/DSASheet'
import {
  Compass,
  MessageSquare,
  BookOpen,
  Edit3,
  User,
  LogOut,
  Sparkles,
  Trophy,
  CheckCircle2,
  Flame,
  ArrowRight,
  Menu,
  X,
  Code2,
  ChevronRight,
  FolderPlus,
  Zap
} from 'lucide-react'

const STRIVER_AZ_URL = 'https://takeuforward.org/dsa/strivers-a2z-sheet-learn-dsa-a-to-z'

const defaultStriverTopics = [
  {
    name: 'Arrays',
    total: 30,
    done: 16,
    problems: ['Two Sum', 'Best Time to Buy and Sell Stock', 'Kadane’s Algorithm', 'Maximum Subarray', 'Merge Overlapping Subintervals', 'Next Permutation'],
  },
  {
    name: 'Hashing',
    total: 18,
    done: 10,
    problems: ['Contains Duplicate', 'Valid Anagram', 'Top K Frequent Elements', 'Longest Consecutive Sequence', 'Subarray Sum Equals K'],
  },
  {
    name: 'Two Pointers',
    total: 16,
    done: 9,
    problems: ['Pair Sum', 'Container With Most Water', '3Sum', 'Remove Duplicates', 'Trapping Rain Water'],
  },
  {
    name: 'Strings',
    total: 22,
    done: 11,
    problems: ['Valid Palindrome', 'Longest Substring Without Repeating', 'String Matching', 'Group Anagrams', 'Minimum Window Substring'],
  },
  {
    name: 'Sliding Window',
    total: 14,
    done: 7,
    problems: ['Maximum Sum Subarray of Size K', 'Longest Subarray with K Sum', 'Permutation in String', 'Fruit Into Baskets'],
  },
  {
    name: 'Linked List',
    total: 20,
    done: 8,
    problems: ['Reverse Linked List', 'Middle of the Linked List', 'Cycle Detection (Floyd)', 'Merge Two Sorted Lists', 'LRU Cache Design'],
  },
  {
    name: 'Stacks & Queues',
    total: 18,
    done: 6,
    problems: ['Valid Parentheses', 'Largest Rectangle in Histogram', 'Implement Queue using Stacks', 'Next Greater Element', 'Daily Temperatures'],
  },
  {
    name: 'Binary Search',
    total: 16,
    done: 10,
    problems: ['Search in Rotated Sorted Array', 'Aggressive Cows', 'First Bad Version', 'Sqrt(x)', 'Koko Eating Bananas'],
  },
  {
    name: 'Binary Trees',
    total: 24,
    done: 9,
    problems: ['Level Order Traversal', 'Validate BST', 'Diameter of Tree', 'Lowest Common Ancestor', 'Maximum Path Sum'],
  },
  {
    name: 'Greedy',
    total: 18,
    done: 5,
    problems: ['Activity Selection', 'Gas Station', 'Jump Game', 'Candy', 'Non-overlapping Intervals'],
  },
  {
    name: 'Backtracking',
    total: 16,
    done: 4,
    problems: ['N-Queens', 'Subset Sum', 'Combination Sum', 'Permutations', 'Word Search'],
  },
  {
    name: 'Graphs',
    total: 24,
    done: 7,
    problems: ['Number of Islands', 'Course Schedule (Topological Sort)', 'Dijkstra’s Algorithm', 'Shortest Path in DAG', 'Bipartite Graph'],
  },
  {
    name: 'Dynamic Programming',
    total: 28,
    done: 6,
    problems: ['Climbing Stairs', 'Coin Change', 'House Robber', 'Longest Increasing Subsequence', '0/1 Knapsack', 'Edit Distance'],
  },
  {
    name: 'Heap & Priority Queue',
    total: 12,
    done: 3,
    problems: ['Kth Largest Element in Array', 'Merge K Sorted Lists', 'Top K Frequent Elements', 'Find Median from Data Stream'],
  },
  {
    name: 'Trie',
    total: 12,
    done: 2,
    problems: ['Implement Trie', 'Word Search II', 'Maximum XOR of Two Numbers', 'Prefix Search'],
  },
  {
    name: 'Bit Manipulation',
    total: 12,
    done: 3,
    problems: ['Count Set Bits (Brian Kernighan)', 'Single Number', 'Power of Two', 'Bitwise AND of Numbers Range'],
  },
]

const STORAGE_KEY = 'algomentor-user'
const USERS_KEY = 'algomentor-users'
const PROGRESS_KEY_PREFIX = 'algomentor-progress-'
const S_NOTES_KEY_PREFIX = 'algomentor-snotes-'

const normalizeEmail = (email) => (email || 'guest').trim().toLowerCase()

const getNotesStorageKey = (email) => `${S_NOTES_KEY_PREFIX}${normalizeEmail(email)}`

const defaultSampleNotes = [
  {
    id: 'sample-1',
    title: 'Sliding Window Pattern & Two Pointers Template',
    content: `
      <h2>Sliding Window Core Blueprint</h2>
      <p>Used for contiguous sequences (subarrays or substrings) to avoid O(N²) quadratic nested loops.</p>
      <div class="samsung-checklist-item" style="display:flex; align-items:center; gap:8px; margin: 6px 0;">
        <input type="checkbox" checked class="checklist-box" style="width:18px; height:18px; accent-color:#6366f1;" />
        <span>Fixed Window: Maintain right - left + 1 == K</span>
      </div>
      <div class="samsung-checklist-item" style="display:flex; align-items:center; gap:8px; margin: 6px 0;">
        <input type="checkbox" checked class="checklist-box" style="width:18px; height:18px; accent-color:#6366f1;" />
        <span>Dynamic Window: Expand right, shrink left when condition violates</span>
      </div>
      <h2>Python Code Template</h2>
      <pre style="background:rgba(0,0,0,0.3); padding:12px; border-radius:8px;"><code>def sliding_window(nums, k):
    left = 0
    current_sum = 0
    max_len = 0
    for right in range(len(nums)):
        current_sum += nums[right]
        while current_sum > k:
            current_sum -= nums[left]
            left += 1
        max_len = max(max_len, right - left + 1)
    return max_len</code></pre>
      <p><strong>Time Complexity:</strong> O(N) amortized | <strong>Space:</strong> O(1)</p>
    `,
    folder: 'patterns',
    tags: ['#sliding-window', '#arrays', '#templates'],
    isPinned: true,
    isLocked: false,
    paperTemplate: 'grid',
    paperTheme: 'dark-slate',
    updatedAt: new Date(Date.now() - 3600000).toISOString(),
  },
  {
    id: 'sample-2',
    title: 'Kadane’s Algorithm: Maximum Subarray Sum Intuition',
    content: `
      <h2>The Core Dilemma at Each Index i</h2>
      <p>Should we <strong>extend</strong> the previous running subarray sum, or <strong>start fresh</strong> from the current number?</p>
      <p style="background:rgba(99,102,241,0.15); border-left:4px solid #6366f1; padding:10px; border-radius:6px;">
        <code>current_sum = max(nums[i], current_sum + nums[i])</code>
      </p>
      <h2>Interview Checklist</h2>
      <div class="samsung-checklist-item" style="display:flex; align-items:center; gap:8px; margin: 6px 0;">
        <input type="checkbox" checked class="checklist-box" style="width:18px; height:18px; accent-color:#6366f1;" />
        <span>Handles all negative numbers? (Initialize max_sum to nums[0], not 0)</span>
      </div>
      <div class="samsung-checklist-item" style="display:flex; align-items:center; gap:8px; margin: 6px 0;">
        <input type="checkbox" checked class="checklist-box" style="width:18px; height:18px; accent-color:#6366f1;" />
        <span>Returns indices if requested (track start and end pointers)</span>
      </div>
    `,
    folder: 'solutions',
    tags: ['#dp', '#kadane', '#faang'],
    isPinned: false,
    isLocked: false,
    paperTemplate: 'ruled',
    paperTheme: 'dark-slate',
    updatedAt: new Date(Date.now() - 7200000).toISOString(),
  },
]

const getSavedNotesForUser = (email) => {
  const key = getNotesStorageKey(email)
  const raw = localStorage.getItem(key)
  if (!raw) return defaultSampleNotes
  try {
    const parsed = JSON.parse(raw)
    return Array.isArray(parsed) && parsed.length ? parsed : defaultSampleNotes
  } catch (err) {
    return defaultSampleNotes
  }
}

const saveNotesForUser = (email, notes) => {
  const key = getNotesStorageKey(email)
  localStorage.setItem(key, JSON.stringify(notes))
}

const normalizeSheetProgress = (progress) => {
  if (!Array.isArray(progress)) {
    return defaultStriverTopics.map((topic) => ({
      ...topic,
      solved: topic.problems.map((_, index) => index < topic.done),
      total: topic.problems.length,
      done: topic.done,
    }))
  }

  return defaultStriverTopics.map((defaultTopic) => {
    const savedTopic = progress.find((item) => item?.name === defaultTopic.name)
    const problems = Array.isArray(savedTopic?.problems) && savedTopic.problems.length
      ? savedTopic.problems
      : defaultTopic.problems
    const existingSolved = Array.isArray(savedTopic?.solved) ? savedTopic.solved : []
    const solved = problems.map((_, index) => {
      if (existingSolved[index] !== undefined) return Boolean(existingSolved[index])
      const defaultDone = Number(savedTopic?.done ?? defaultTopic.done) || 0
      return index < Math.min(Math.max(defaultDone, 0), problems.length)
    })

    return {
      ...defaultTopic,
      ...savedTopic,
      name: defaultTopic.name,
      total: problems.length,
      done: solved.filter(Boolean).length,
      problems,
      solved,
    }
  })
}

const getStoredUsers = () => {
  const raw = localStorage.getItem(USERS_KEY)
  if (!raw) return {}
  try {
    const parsed = JSON.parse(raw)
    return parsed && typeof parsed === 'object' ? parsed : {}
  } catch {
    return {}
  }
}

const getProgressForEmail = (email) => {
  if (!email) return defaultStriverTopics
  const raw = localStorage.getItem(`${PROGRESS_KEY_PREFIX}${normalizeEmail(email)}`)
  if (!raw) return defaultStriverTopics
  try {
    const parsed = JSON.parse(raw)
    if (Array.isArray(parsed) && parsed.length) return normalizeSheetProgress(parsed)
  } catch {}
  return defaultStriverTopics
}

const saveProgressForEmail = (email, progress) => {
  if (!email) return
  localStorage.setItem(`${PROGRESS_KEY_PREFIX}${normalizeEmail(email)}`, JSON.stringify(progress))
}

export default function App() {
  const [activeView, setActiveView] = useState('home') // 'home' | 'sheet' | 'chat' | 'notes' | 'login' | 'signup'
  const [mobileNavOpen, setMobileNavOpen] = useState(false)
  const [chatInitialPrompt, setChatInitialPrompt] = useState('')

  const [loggedUser, setLoggedUser] = useState(() => {
    const saved = localStorage.getItem(STORAGE_KEY)
    return saved ? JSON.parse(saved) : null
  })

  const [sheetProgress, setSheetProgress] = useState(() => getProgressForEmail(loggedUser?.email))
  const [notes, setNotes] = useState(() => getSavedNotesForUser(loggedUser?.email))
  const [activeNoteId, setActiveNoteId] = useState(null)

  // Auth form states
  const [loginForm, setLoginForm] = useState({ email: '', password: '' })
  const [signupForm, setSignupForm] = useState({ name: '', email: '', password: '' })
  const [authError, setAuthError] = useState('')
  const [authMessage, setAuthMessage] = useState('')

  // Sync state on user change
  useEffect(() => {
    if (loggedUser?.email) {
      setSheetProgress(getProgressForEmail(loggedUser.email))
      setNotes(getSavedNotesForUser(loggedUser.email))
      localStorage.setItem(STORAGE_KEY, JSON.stringify(loggedUser))
    }
  }, [loggedUser])

  // Save sheet progress
  useEffect(() => {
    if (loggedUser?.email) {
      saveProgressForEmail(loggedUser.email, sheetProgress)
    }
  }, [sheetProgress, loggedUser])

  // Save notes
  useEffect(() => {
    saveNotesForUser(loggedUser?.email, notes)
  }, [notes, loggedUser])

  const totalDone = useMemo(
    () => sheetProgress.reduce((sum, topic) => sum + (topic.solved?.filter(Boolean).length ?? topic.done ?? 0), 0),
    [sheetProgress]
  )
  const totalQuestions = useMemo(
    () => sheetProgress.reduce((sum, topic) => sum + (topic.problems?.length ?? topic.total ?? 0), 0),
    [sheetProgress]
  )
  const completionPercent = totalQuestions ? Math.round((totalDone / totalQuestions) * 100) : 0

  const handleProblemToggle = (topicIndex, problemIndex) => {
    setSheetProgress((current) =>
      current.map((topic, index) => {
        if (index !== topicIndex) return topic

        const nextSolved = (topic.solved ?? topic.problems.map((_, itemIndex) => itemIndex < (topic.done ?? 0))).map((val, itemIndex) =>
          itemIndex === problemIndex ? !val : val
        )

        return {
          ...topic,
          solved: nextSolved,
          done: nextSolved.filter(Boolean).length,
          total: topic.problems.length,
        }
      })
    )
  }

  // Save or update note from SamsungNotes component
  const handleSaveNote = (updatedNote) => {
    setNotes((prev) => {
      const idx = prev.findIndex((n) => n.id === updatedNote.id)
      if (idx >= 0) {
        const next = [...prev]
        next[idx] = updatedNote
        return next
      }
      return [updatedNote, ...prev]
    })
  }

  const handleDeleteNote = (noteId) => {
    setNotes((prev) => prev.filter((n) => n.id !== noteId))
    setActiveNoteId(null)
  }

  const handleDuplicateNote = (note) => {
    const dup = {
      ...note,
      id: `note-${Date.now()}`,
      title: `${note.title} (Copy)`,
      updatedAt: new Date().toISOString(),
    }
    setNotes((prev) => [dup, ...prev])
    setActiveNoteId(dup.id)
  }

  // Save AI answer directly into Samsung Notes
  const handleSaveAIToNotes = ({ title, content, category, tags }) => {
    const newNote = {
      id: `note-${Date.now()}`,
      title: title || 'AI Explanation Note',
      content: content.replace(/\n/g, '<br/>'),
      folder: 'patterns',
      tags: tags || ['#ai-mentor', '#dsa'],
      isPinned: false,
      isLocked: false,
      paperTemplate: 'grid',
      paperTheme: 'dark-slate',
      updatedAt: new Date().toISOString(),
    }
    setNotes((prev) => [newNote, ...prev])
    setActiveNoteId(newNote.id)
  }

  // Ask AI about a problem from DSA Sheet
  const handleAskAIAboutProblem = (problemName) => {
    setChatInitialPrompt(`How do I solve ${problemName}? Identify the pattern, step-by-step intuition, and optimal approach.`)
    setActiveView('chat')
  }

  // Auth handlers
  const handleLogin = (e) => {
    e.preventDefault()
    const email = normalizeEmail(loginForm.email)
    const password = loginForm.password

    if (!email || !password) {
      setAuthError('Please enter your email and password.')
      return
    }

    const users = getStoredUsers()
    const user = users[email]
    if (!user) {
      setAuthError('No account found with this email. Please sign up.')
      return
    }
    if (user.password !== password) {
      setAuthError('Incorrect password. Please try again.')
      return
    }

    setLoggedUser(user)
    setAuthMessage(`Welcome back, ${user.name}!`)
    setAuthError('')
    setActiveView('home')
  }

  const handleSignup = (e) => {
    e.preventDefault()
    const name = signupForm.name.trim()
    const email = normalizeEmail(signupForm.email)
    const password = signupForm.password

    if (!name || !email || !password) {
      setAuthError('Please complete all fields.')
      return
    }

    const users = getStoredUsers()
    if (users[email]) {
      setAuthError('An account with this email already exists. Please log in.')
      return
    }

    const newUser = { name, email, password }
    users[email] = newUser
    localStorage.setItem(USERS_KEY, JSON.stringify(users))
    setLoggedUser(newUser)
    setAuthMessage(`Account created! Welcome, ${name}.`)
    setAuthError('')
    setActiveView('home')
  }

  const handleLogout = () => {
    localStorage.removeItem(STORAGE_KEY)
    setLoggedUser(null)
    setAuthMessage('Logged out successfully.')
    setActiveView('home')
  }

  return (
    <div className="app-shell">
      {/* PROFESSIONAL SLATE TOPBAR */}
      <header className="app-topbar">
        <div className="topbar-inner">
          <div className="brand-group" onClick={() => setActiveView('home')} style={{ cursor: 'pointer' }}>
            <div className="brand-badge">
              <Zap size={20} className="text-white" />
            </div>
            <div className="brand-text">
              <span className="brand-name">AlgoMentor</span>
              <span className="brand-tagline">Pro Edition</span>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="desktop-nav">
            <button
              type="button"
              className={`nav-link ${activeView === 'home' ? 'active' : ''}`}
              onClick={() => setActiveView('home')}
            >
              Overview
            </button>
            <button
              type="button"
              className={`nav-link ${activeView === 'sheet' ? 'active' : ''}`}
              onClick={() => setActiveView('sheet')}
            >
              DSA Sheets
            </button>
            <button
              type="button"
              className={`nav-link ${activeView === 'chat' ? 'active' : ''}`}
              onClick={() => setActiveView('chat')}
            >
              AI Mentor
            </button>
            <button
              type="button"
              className={`nav-link ${activeView === 'notes' ? 'active' : ''}`}
              onClick={() => setActiveView('notes')}
            >
              Samsung Notes
            </button>
          </nav>

          {/* Right User Actions */}
          <div className="topbar-right">
            {loggedUser ? (
              <div className="user-profile-badge">
                <div className="user-avatar-circle">
                  {(loggedUser.name || loggedUser.email)[0].toUpperCase()}
                </div>
                <span className="user-display-name">{loggedUser.name || loggedUser.email}</span>
                <button
                  type="button"
                  className="logout-icon-btn"
                  title="Logout"
                  onClick={handleLogout}
                >
                  <LogOut size={16} />
                </button>
              </div>
            ) : (
              <div className="auth-btns-group">
                <button
                  type="button"
                  className="auth-btn-ghost"
                  onClick={() => setActiveView('login')}
                >
                  Log In
                </button>
                <button
                  type="button"
                  className="auth-btn-primary"
                  onClick={() => setActiveView('signup')}
                >
                  Sign Up
                </button>
              </div>
            )}

            {/* Mobile Hamburger Toggle */}
            <button
              type="button"
              className="mobile-menu-toggle"
              onClick={() => setMobileNavOpen(!mobileNavOpen)}
              aria-label="Toggle navigation menu"
            >
              {mobileNavOpen ? <X size={22} /> : <Menu size={22} />}
            </button>
          </div>
        </div>

        {/* Mobile Navigation Drawer */}
        {mobileNavOpen && (
          <div className="mobile-drawer">
            <button
              type="button"
              className={`mobile-drawer-link ${activeView === 'home' ? 'active' : ''}`}
              onClick={() => { setActiveView('home'); setMobileNavOpen(false) }}
            >
              Overview
            </button>
            <button
              type="button"
              className={`mobile-drawer-link ${activeView === 'sheet' ? 'active' : ''}`}
              onClick={() => { setActiveView('sheet'); setMobileNavOpen(false) }}
            >
              DSA Sheets ({completionPercent}%)
            </button>
            <button
              type="button"
              className={`mobile-drawer-link ${activeView === 'chat' ? 'active' : ''}`}
              onClick={() => { setActiveView('chat'); setMobileNavOpen(false) }}
            >
              AI Mentor Chat
            </button>
            <button
              type="button"
              className={`mobile-drawer-link ${activeView === 'notes' ? 'active' : ''}`}
              onClick={() => { setActiveView('notes'); setMobileNavOpen(false) }}
            >
              Samsung Notes ({notes.length})
            </button>
            {!loggedUser ? (
              <div className="mobile-auth-row">
                <button type="button" className="auth-btn-ghost w-full" onClick={() => { setActiveView('login'); setMobileNavOpen(false) }}>Log In</button>
                <button type="button" className="auth-btn-primary w-full" onClick={() => { setActiveView('signup'); setMobileNavOpen(false) }}>Sign Up</button>
              </div>
            ) : (
              <button type="button" className="mobile-drawer-link text-rose-400" onClick={() => { handleLogout(); setMobileNavOpen(false) }}>Log Out</button>
            )}
          </div>
        )}
      </header>

      {/* NOTIFICATION BANNER */}
      {authMessage && (
        <div className="app-banner-notification">
          <span>{authMessage}</span>
          <button type="button" onClick={() => setAuthMessage('')}>✕</button>
        </div>
      )}

      {/* MAIN VIEWPORT */}
      <main className="app-main-content">
        {/* 1. HOME VIEW */}
        {activeView === 'home' && (
          <div className="home-dashboard">
            {/* Hero Section */}
            <section className="hero-pro-section">
              <div className="hero-pro-badge">
                <Sparkles size={14} className="text-indigo-400" />
                <span>Next-Gen Agentic DSA Preparation</span>
              </div>
              <h1 className="hero-pro-heading">
                Master Algorithms with <span className="gradient-text">Precision & Intuition</span>
              </h1>
              <p className="hero-pro-sub">
                Follow Striver’s structured A-to-Z roadmap, get instant ChatGPT-grade explanations from AlgoMentor AI,
                and capture visual problem solutions with Samsung Notes.
              </p>

              <div className="hero-cta-row">
                <button
                  type="button"
                  className="hero-primary-cta"
                  onClick={() => setActiveView('sheet')}
                >
                  <span>Explore DSA Sheets</span>
                  <ArrowRight size={17} />
                </button>
                <button
                  type="button"
                  className="hero-secondary-cta"
                  onClick={() => setActiveView('chat')}
                >
                  <MessageSquare size={17} />
                  <span>Start AI Chat</span>
                </button>
                <button
                  type="button"
                  className="hero-secondary-cta"
                  onClick={() => setActiveView('notes')}
                >
                  <Edit3 size={17} />
                  <span>Open Samsung Notes</span>
                </button>
              </div>
            </section>

            {/* Quick Metrics Bar */}
            <div className="home-metrics-bar">
              <div className="metric-card">
                <div className="metric-icon-wrap indigo">
                  <CheckCircle2 size={22} />
                </div>
                <div>
                  <div className="metric-number">{totalDone} / {totalQuestions}</div>
                  <div className="metric-label">Problems Solved ({completionPercent}%)</div>
                </div>
              </div>

              <div className="metric-card">
                <div className="metric-icon-wrap emerald">
                  <Flame size={22} />
                </div>
                <div>
                  <div className="metric-number">{defaultStriverTopics.length} Topics</div>
                  <div className="metric-label">Striver A-Z Roadmap</div>
                </div>
              </div>

              <div className="metric-card">
                <div className="metric-icon-wrap violet">
                  <Edit3 size={22} />
                </div>
                <div>
                  <div className="metric-number">{notes.length} Notes</div>
                  <div className="metric-label">Samsung Notes Created</div>
                </div>
              </div>
            </div>

            {/* Feature Cards Grid */}
            <div className="home-feature-cards">
              <div className="feature-card" onClick={() => setActiveView('sheet')}>
                <div className="feature-card-header">
                  <div className="feature-icon bg-blue">
                    <BookOpen size={24} />
                  </div>
                  <span className="feature-badge">Curated Roadmap</span>
                </div>
                <h3>Striver’s A-to-Z DSA Sheet</h3>
                <p>
                  Practice step-by-step from Foundation arrays and hashing up to Dynamic Programming,
                  Segment Trees, and Graphs. Interactive checkboxes with confetti celebration.
                </p>
                <div className="feature-card-link">
                  <span>Open DSA Sheet</span>
                  <ChevronRight size={16} />
                </div>
              </div>

              <div className="feature-card" onClick={() => setActiveView('chat')}>
                <div className="feature-card-header">
                  <div className="feature-icon bg-violet">
                    <MessageSquare size={24} />
                  </div>
                  <span className="feature-badge">ChatGPT-Grade AI</span>
                </div>
                <h3>AlgoMentor AI Chat</h3>
                <p>
                  Ask any DSA question, request optimal code, simulate FAANG mock interviews,
                  or ask for progressive hints. Fully multi-turn with code copy and complexity breakdowns.
                </p>
                <div className="feature-card-link">
                  <span>Launch AI Mentor</span>
                  <ChevronRight size={16} />
                </div>
              </div>

              <div className="feature-card" onClick={() => setActiveView('notes')}>
                <div className="feature-card-header">
                  <div className="feature-icon bg-indigo">
                    <Edit3 size={24} />
                  </div>
                  <span className="feature-badge">Samsung Notes Experience</span>
                </div>
                <h3>Samsung Notes Suite</h3>
                <p>
                  Rich text formatting, S-Pen handwriting sketch canvas, paper templates (grid, ruled, dot),
                  highlighter markers, audio memos, checklists, PIN lock, and multi-format export.
                </p>
                <div className="feature-card-link">
                  <span>Open Samsung Notes</span>
                  <ChevronRight size={16} />
                </div>
              </div>
            </div>
          </div>
        )}

        {/* 2. DSA SHEET VIEW */}
        {activeView === 'sheet' && (
          <DSASheet
            sheetProgress={sheetProgress}
            onToggleProblem={handleProblemToggle}
            onAskAIAboutProblem={handleAskAIAboutProblem}
            loggedUser={loggedUser}
          />
        )}

        {/* 3. AI CHAT VIEW */}
        {activeView === 'chat' && (
          <AIChat
            onSaveToNotes={handleSaveAIToNotes}
            onOpenNotes={() => setActiveView('notes')}
            loggedUser={loggedUser}
            initialPrompt={chatInitialPrompt}
            onClearInitialPrompt={() => setChatInitialPrompt('')}
          />
        )}

        {/* 4. SAMSUNG NOTES VIEW */}
        {activeView === 'notes' && (
          <SamsungNotes
            notes={notes}
            activeNoteId={activeNoteId}
            onSelectNote={(id) => setActiveNoteId(id)}
            onSaveNote={handleSaveNote}
            onDeleteNote={handleDeleteNote}
            onDuplicateNote={handleDuplicateNote}
            loggedUser={loggedUser}
          />
        )}

        {/* 5. AUTH LOGIN VIEW */}
        {activeView === 'login' && (
          <div className="auth-card-wrapper">
            <div className="auth-card-inner">
              <button type="button" className="auth-back-link" onClick={() => setActiveView('home')}>
                ← Back to Overview
              </button>
              <h2>Welcome Back</h2>
              <p className="auth-subtitle">Log in to sync your DSA progress and Samsung Notes across sessions.</p>

              <form onSubmit={handleLogin} className="auth-form-body">
                <div className="form-field">
                  <label>Email Address</label>
                  <input
                    type="email"
                    value={loginForm.email}
                    onChange={(e) => setLoginForm((p) => ({ ...p, email: e.target.value }))}
                    placeholder="student@example.com"
                    required
                  />
                </div>

                <div className="form-field">
                  <label>Password</label>
                  <input
                    type="password"
                    value={loginForm.password}
                    onChange={(e) => setLoginForm((p) => ({ ...p, password: e.target.value }))}
                    placeholder="••••••••"
                    required
                  />
                </div>

                {authError && <div className="auth-error-pill">{authError}</div>}

                <button type="submit" className="auth-submit-btn">
                  Log In
                </button>
              </form>

              <div className="auth-switch-prompt">
                Don’t have an account yet?{' '}
                <button type="button" onClick={() => { setAuthError(''); setActiveView('signup') }}>
                  Create Account
                </button>
              </div>
            </div>
          </div>
        )}

        {/* 6. AUTH SIGNUP VIEW */}
        {activeView === 'signup' && (
          <div className="auth-card-wrapper">
            <div className="auth-card-inner">
              <button type="button" className="auth-back-link" onClick={() => setActiveView('home')}>
                ← Back to Overview
              </button>
              <h2>Create Account</h2>
              <p className="auth-subtitle">Join AlgoMentor to track problems, take notes, and get AI guidance.</p>

              <form onSubmit={handleSignup} className="auth-form-body">
                <div className="form-field">
                  <label>Full Name</label>
                  <input
                    type="text"
                    value={signupForm.name}
                    onChange={(e) => setSignupForm((p) => ({ ...p, name: e.target.value }))}
                    placeholder="Alex Student"
                    required
                  />
                </div>

                <div className="form-field">
                  <label>Email Address</label>
                  <input
                    type="email"
                    value={signupForm.email}
                    onChange={(e) => setSignupForm((p) => ({ ...p, email: e.target.value }))}
                    placeholder="student@example.com"
                    required
                  />
                </div>

                <div className="form-field">
                  <label>Password</label>
                  <input
                    type="password"
                    value={signupForm.password}
                    onChange={(e) => setSignupForm((p) => ({ ...p, password: e.target.value }))}
                    placeholder="At least 6 characters"
                    required
                  />
                </div>

                {authError && <div className="auth-error-pill">{authError}</div>}

                <button type="submit" className="auth-submit-btn">
                  Create Account
                </button>
              </form>

              <div className="auth-switch-prompt">
                Already have an account?{' '}
                <button type="button" onClick={() => { setAuthError(''); setActiveView('login') }}>
                  Log In
                </button>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
