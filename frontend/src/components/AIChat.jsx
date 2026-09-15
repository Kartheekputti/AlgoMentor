import { useState, useRef, useEffect } from 'react'
import {
  Bot,
  User,
  Send,
  Sparkles,
  Copy,
  Check,
  RotateCcw,
  Trash2,
  Settings,
  Code2,
  Compass,
  Briefcase,
  Lightbulb,
  FilePlus2,
  Flame,
  ChevronDown,
  Layers,
  ArrowRight,
  Code,
  ListOrdered,
  BookOpen
} from 'lucide-react'

const MODES = [
  { id: 'concept', label: 'Mentor', icon: Compass, description: 'Socratic hints & conceptual intuition' },
  { id: 'code', label: 'Code & Optimal', icon: Code2, description: 'Production code & complexity analysis' },
  { id: 'problem-analysis', label: 'Pattern Finder', icon: Layers, description: 'Identify pattern, constraints & approach' },
  { id: 'interview', label: 'Mock Interview', icon: Briefcase, description: 'FAANG interview scenario & critique' },
  { id: 'hint', label: 'Progressive Hints', icon: Lightbulb, description: '5-level step-by-step guidance' },
]

const LANGUAGES = [
  { id: 'python', label: 'Python' },
  { id: 'java', label: 'Java' },
  { id: 'cpp', label: 'C++' },
  { id: 'javascript', label: 'JavaScript' },
]

const HINT_TIERS = [
  { level: 1, label: '1. Observation', desc: 'General observation' },
  { level: 2, label: '2. Data Structure', desc: 'Appropriate data structure' },
  { level: 3, label: '3. Approach', desc: 'Core algorithmic approach' },
  { level: 4, label: '4. Algorithm', desc: 'Step-by-step logic' },
  { level: 5, label: '5. Full Solution', desc: 'Complete code & complexity' },
]

const PROMPT_SUGGESTIONS = [
  {
    category: 'Pattern Finder',
    prompt: 'How do I solve Trapping Rain Water? Identify the pattern and explain both Two Pointers and Monotonic Stack approaches.',
  },
  {
    category: 'Dynamic Programming',
    prompt: 'Explain Kadane’s Algorithm visually with a step-by-step example and time complexity.',
  },
  {
    category: 'Progressive Hints',
    prompt: 'Give me Level 1 hint for solving Two Sum in O(N) time without giving away the full code.',
  },
  {
    category: 'System & Design',
    prompt: 'Explain how to implement an LRU Cache with O(1) get and put operations in Java and Python.',
  },
  {
    category: 'Graphs & TopoSort',
    prompt: 'Explain Course Schedule problem and how Kahn’s Algorithm detects cycles in a Directed Graph.',
  },
  {
    category: 'Mock Interview',
    prompt: 'Simulate a FAANG technical interview for finding the Median of Two Sorted Arrays. Ask me clarifying questions.',
  },
]

export default function AIChat({ onSaveToNotes, onOpenNotes, loggedUser, initialPrompt, onClearInitialPrompt }) {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content:
        `Hello! I'm **AlgoMentor**, your personal Agentic DSA & Interview reasoning mentor inspired by ChatGPT.\n\n` +
        `I can help you:\n` +
        `* 🧠 **Pattern Recognition:** Instantly identify whether a problem needs Sliding Window, Two Pointers, Monotonic Stack, or DP\n` +
        `* 💡 **5-Level Progressive Hints:** Get gentle clues step-by-step without spoiling the full solution\n` +
        `* 💻 **Multi-Language Solutions:** Optimal production implementations in **Java**, **Python**, **C++**, or **JavaScript**\n` +
        `* 📊 **Personalized Practice & Progress:** Ask *"Analyze my progress"* or *"Create a practice plan"* tailored to your solved problems\n` +
        `* 📝 Save any explanation or code block directly into your **Samsung Notes**!\n\n` +
        `What topic or problem would you like to explore today?`,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [mode, setMode] = useState('concept')
  const [language, setLanguage] = useState(() => localStorage.getItem('algomentor-lang') || 'python')
  const [currentHintLevel, setCurrentHintLevel] = useState(1)
  const [copiedCodeKey, setCopiedCodeKey] = useState(null)
  const [copiedMessageIndex, setCopiedMessageIndex] = useState(null)
  const [saveToast, setSaveToast] = useState(null)
  const [showSettings, setShowSettings] = useState(false)
  const [apiKey, setApiKey] = useState(() => localStorage.getItem('algomentor-api-key') || '')
  const [provider, setProvider] = useState(() => localStorage.getItem('algomentor-provider') || 'ollama')
  const [ollamaModel, setOllamaModel] = useState(() => localStorage.getItem('algomentor-ollama-model') || 'llama3.2')

  const messagesEndRef = useRef(null)
  const textareaRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, loading])

  useEffect(() => {
    if (initialPrompt && initialPrompt.trim()) {
      handleSendMessage(initialPrompt)
      if (onClearInitialPrompt) onClearInitialPrompt()
    }
  }, [initialPrompt])

  const handleLanguageChange = (newLang) => {
    setLanguage(newLang)
    localStorage.setItem('algomentor-lang', newLang)
  }

  const handleSaveSettings = () => {
    localStorage.setItem('algomentor-api-key', apiKey)
    localStorage.setItem('algomentor-provider', provider)
    localStorage.setItem('algomentor-ollama-model', ollamaModel)
    setShowSettings(false)
  }

  const handleSendMessage = async (textToSend = null, customHintLevel = null) => {
    const text = (typeof textToSend === 'string' ? textToSend : input).trim()
    if (!text || loading) return

    const userMessage = {
      role: 'user',
      content: text,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    }

    const nextMessages = [...messages, userMessage]
    setMessages(nextMessages)
    setInput('')
    setLoading(true)

    const historyPayload = nextMessages.slice(-8).map((m) => ({
      role: m.role,
      content: m.content,
    }))

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: text,
          mode: mode,
          history: historyPayload,
          api_key: apiKey ? apiKey.trim() : null,
          provider: provider !== 'ollama' && apiKey ? provider : null,
          user_email: loggedUser?.email || null,
          language: language,
          hint_level: customHintLevel || (mode === 'hint' ? currentHintLevel : null),
        }),
      })

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
      }

      const data = await response.json()
      if (data.hint_level) {
        setCurrentHintLevel(data.hint_level)
      }

      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: data.response,
          sources: data.sources || [],
          mode: data.mode,
          pattern: data.pattern,
          hint_level: data.hint_level,
          suggested_next_actions: data.suggested_next_actions || [],
          similar_problems: data.similar_problems || [],
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        },
      ])
    } catch (err) {
      console.error('Chat error:', err)
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content:
            `⚠️ **Connection Note:** The AlgoMentor backend service is busy or offline.\n\n` +
            `Ensure the backend is running (` + '`python -m uvicorn main:app --reload`' + ` on port 8000) or check your model settings.`,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        },
      ])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const copyToClipboard = (text, key, isMessage = false) => {
    navigator.clipboard.writeText(text)
    if (isMessage) {
      setCopiedMessageIndex(key)
      setTimeout(() => setCopiedMessageIndex(null), 2000)
    } else {
      setCopiedCodeKey(key)
      setTimeout(() => setCopiedCodeKey(null), 2000)
    }
  }

  const handleSaveMessageToNotes = (msg) => {
    if (!onSaveToNotes) return
    const lines = msg.content.split('\n')
    let title = 'AI Note: DSA Concept'
    for (const l of lines) {
      const clean = l.replace(/^[#*\s]+/, '').trim()
      if (clean.length > 3 && clean.length < 60) {
        title = clean
        break
      }
    }

    onSaveToNotes({
      title: title,
      content: msg.content,
      category: 'DSA Patterns',
      tags: ['#ai-mentor', '#dsa'],
    })

    setSaveToast('Saved to Samsung Notes!')
    setTimeout(() => setSaveToast(null), 3000)
  }

  const handleClearChat = () => {
    if (window.confirm('Clear all conversation messages?')) {
      setMessages([
        {
          role: 'assistant',
          content: "Chat cleared. What DSA topic or algorithm would you like to explore next?",
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        },
      ])
      setCurrentHintLevel(1)
    }
  }

  const renderMessageContent = (content, msgIndex) => {
    const parts = content.split(/(```[\s\S]*?```)/g)

    return parts.map((part, pIdx) => {
      if (part.startsWith('```') && part.endsWith('```')) {
        const lines = part.slice(3, -3).trim().split('\n')
        let langTag = 'code'
        let codeBody = part.slice(3, -3).trim()
        if (lines[0] && !lines[0].includes(' ') && lines[0].length < 15) {
          langTag = lines[0].toLowerCase()
          codeBody = lines.slice(1).join('\n')
        }

        const blockKey = `${msgIndex}-${pIdx}`
        const isCopied = copiedCodeKey === blockKey

        return (
          <div key={blockKey} className="chat-code-block">
            <div className="chat-code-header">
              <span className="code-lang-tag">{langTag}</span>
              <button
                type="button"
                className="code-copy-btn"
                onClick={() => copyToClipboard(codeBody, blockKey)}
              >
                {isCopied ? <Check size={14} className="text-emerald-400" /> : <Copy size={14} />}
                <span>{isCopied ? 'Copied' : 'Copy code'}</span>
              </button>
            </div>
            <pre className="chat-code-body">
              <code>{codeBody}</code>
            </pre>
          </div>
        )
      }

      return (
        <div key={pIdx} className="chat-text-chunk">
          {part.split('\n\n').map((para, paraIdx) => {
            if (!para.trim()) return null

            if (para.startsWith('### ')) {
              return <h4 key={paraIdx} className="chat-h4">{para.replace('### ', '')}</h4>
            }
            if (para.startsWith('## ')) {
              return <h3 key={paraIdx} className="chat-h3">{para.replace('## ', '')}</h3>
            }
            if (para.startsWith('# ')) {
              return <h2 key={paraIdx} className="chat-h2">{para.replace('# ', '')}</h2>
            }

            if (para.startsWith('* ') || para.startsWith('- ') || /^\d+\.\s/.test(para)) {
              const items = para.split('\n')
              return (
                <ul key={paraIdx} className="chat-list">
                  {items.map((item, iIdx) => {
                    const cleanItem = item.replace(/^([*\-]\s|\d+\.\s)/, '')
                    return <li key={iIdx}>{formatInlineMarkdown(cleanItem)}</li>
                  })}
                </ul>
              )
            }

            return <p key={paraIdx} className="chat-p">{formatInlineMarkdown(para)}</p>
          })}
        </div>
      )
    })
  }

  const formatInlineMarkdown = (text) => {
    const parts = text.split(/(`[^`]+`|\*\*[^*]+\*\*|\$[^$]+\$)/g)
    return parts.map((seg, sIdx) => {
      if (seg.startsWith('`') && seg.endsWith('`')) {
        return <code key={sIdx} className="chat-inline-code">{seg.slice(1, -1)}</code>
      }
      if (seg.startsWith('**') && seg.endsWith('**')) {
        return <strong key={sIdx} className="chat-strong">{seg.slice(2, -2)}</strong>
      }
      if (seg.startsWith('$') && seg.endsWith('$')) {
        return <span key={sIdx} className="chat-complexity-badge">{seg.slice(1, -1)}</span>
      }
      return seg
    })
  }

  return (
    <div className="chat-container">
      {saveToast && (
        <div className="save-toast">
          <Check size={16} />
          <span>{saveToast}</span>
          <button type="button" className="toast-link" onClick={onOpenNotes}>
            Open Notes →
          </button>
        </div>
      )}

      {/* Top Header */}
      <div className="chat-header-bar">
        <div className="chat-title-group">
          <div className="chat-avatar-brand">
            <Bot size={20} />
          </div>
          <div>
            <div className="chat-brand-title">AlgoMentor AI</div>
            <div className="chat-brand-subtitle">
              <span className="online-indicator"></span>
              {provider === 'ollama' ? `Llama 3.2 (Local Engine)` : `${provider.toUpperCase()} (Cloud AI)`}
              {loggedUser && <span className="user-synced-pill"> • {loggedUser.name || loggedUser.email}</span>}
            </div>
          </div>
        </div>

        <div className="chat-header-actions">
          {/* Language Selector */}
          <div className="chat-lang-selector" title="Preferred Language for Code Solutions">
            <Code size={14} className="text-indigo-400" />
            <select
              value={language}
              onChange={(e) => handleLanguageChange(e.target.value)}
              className="lang-select-dropdown"
            >
              {LANGUAGES.map((l) => (
                <option key={l.id} value={l.id}>{l.label}</option>
              ))}
            </select>
          </div>

          <button
            type="button"
            className="icon-action-btn"
            title="Clear conversation"
            onClick={handleClearChat}
          >
            <Trash2 size={16} />
          </button>
          <button
            type="button"
            className="icon-action-btn"
            title="AI Model & API Key Settings"
            onClick={() => setShowSettings(true)}
          >
            <Settings size={16} />
          </button>
        </div>
      </div>

      {/* Mode Selector */}
      <div className="chat-modes-row">
        {MODES.map((m) => {
          const Icon = m.icon
          const isActive = mode === m.id
          return (
            <button
              key={m.id}
              type="button"
              className={`mode-pill ${isActive ? 'active' : ''}`}
              onClick={() => setMode(m.id)}
              title={m.description}
            >
              <Icon size={14} />
              <span>{m.label}</span>
            </button>
          )
        })}
      </div>

      {/* Progressive Hints Sub-toolbar (Active in Hint mode) */}
      {mode === 'hint' && (
        <div className="hint-stepper-tray">
          <div className="hint-stepper-label">
            <Lightbulb size={13} className="text-amber-400" />
            <span>Progressive Hint Tiers:</span>
          </div>
          <div className="hint-stepper-pills">
            {HINT_TIERS.map((tier) => (
              <button
                key={tier.level}
                type="button"
                className={`hint-tier-btn ${currentHintLevel === tier.level ? 'active' : ''}`}
                onClick={() => {
                  setCurrentHintLevel(tier.level)
                  handleSendMessage(`Give me Hint Level ${tier.level} for this problem`, tier.level)
                }}
                title={tier.desc}
              >
                {tier.label}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Messages Stream */}
      <div className="chat-messages-area">
        {messages.map((msg, idx) => {
          const isUser = msg.role === 'user'
          const isCopied = copiedMessageIndex === idx

          return (
            <div key={idx} className={`chat-bubble-wrap ${isUser ? 'user-wrap' : 'assistant-wrap'}`}>
              <div className="chat-avatar">
                {isUser ? (
                  <div className="avatar-user">
                    <User size={16} />
                  </div>
                ) : (
                  <div className="avatar-assistant">
                    <Bot size={16} />
                  </div>
                )}
              </div>

              <div className="chat-bubble-content">
                <div className="chat-bubble-meta">
                  <span className="bubble-author">{isUser ? 'You' : 'AlgoMentor'}</span>
                  {msg.mode && !isUser && (
                    <span className="bubble-mode-tag">{msg.mode}</span>
                  )}
                  {msg.pattern && !isUser && (
                    <span className="bubble-pattern-pill">
                      <Layers size={11} />
                      <span>{msg.pattern}</span>
                    </span>
                  )}
                  <span className="bubble-time">{msg.timestamp}</span>
                </div>

                <div className="bubble-text">
                  {renderMessageContent(msg.content, idx)}
                </div>

                {/* Similar Problems Tray */}
                {msg.similar_problems && msg.similar_problems.length > 0 && (
                  <div className="bubble-similar-tray">
                    <div className="similar-title">
                      <BookOpen size={13} className="text-indigo-400" />
                      <span>Connected Practice Problems:</span>
                    </div>
                    <div className="similar-chips">
                      {msg.similar_problems.map((prob, pIdx) => (
                        <button
                          key={pIdx}
                          type="button"
                          className="similar-chip"
                          onClick={() => handleSendMessage(`Break down and solve ${prob.title}`)}
                        >
                          <span className="prob-name">{prob.title}</span>
                          <span className={`prob-diff diff-${(prob.difficulty || 'medium').toLowerCase()}`}>
                            {prob.difficulty}
                          </span>
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                {/* Suggested Next Action Chips */}
                {!isUser && msg.suggested_next_actions && msg.suggested_next_actions.length > 0 && (
                  <div className="bubble-suggestions-row">
                    {msg.suggested_next_actions.map((action, aIdx) => (
                      <button
                        key={aIdx}
                        type="button"
                        className="suggestion-action-chip"
                        onClick={() => handleSendMessage(action)}
                      >
                        <Sparkles size={12} className="text-indigo-400" />
                        <span>{action}</span>
                      </button>
                    ))}
                  </div>
                )}

                {/* Sources if present */}
                {msg.sources && msg.sources.length > 0 && (
                  <div className="bubble-sources">
                    <span className="sources-label">Knowledge consulted:</span>
                    {msg.sources.map((src, sIdx) => (
                      <span key={sIdx} className="source-tag">{src}</span>
                    ))}
                  </div>
                )}

                {/* Assistant message action bar */}
                {!isUser && (
                  <div className="bubble-actions">
                    <button
                      type="button"
                      className="bubble-action-btn"
                      onClick={() => copyToClipboard(msg.content, idx, true)}
                      title="Copy response"
                    >
                      {isCopied ? <Check size={13} className="text-emerald-400" /> : <Copy size={13} />}
                      <span>{isCopied ? 'Copied' : 'Copy'}</span>
                    </button>

                    <button
                      type="button"
                      className="bubble-action-btn save-note-action"
                      onClick={() => handleSaveMessageToNotes(msg)}
                      title="Save this answer to Samsung Notes"
                    >
                      <FilePlus2 size={13} />
                      <span>Save to Notes</span>
                    </button>
                  </div>
                )}
              </div>
            </div>
          )
        })}

        {/* Loading typing indicator */}
        {loading && (
          <div className="chat-bubble-wrap assistant-wrap">
            <div className="chat-avatar">
              <div className="avatar-assistant">
                <Bot size={16} />
              </div>
            </div>
            <div className="chat-bubble-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
                <span className="typing-label">AlgoMentor is reasoning...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Suggested prompts tray */}
      {messages.length <= 2 && (
        <div className="suggestions-tray">
          <div className="suggestions-header">
            <Sparkles size={14} />
            <span>Popular DSA Prompts</span>
          </div>
          <div className="suggestions-grid">
            {PROMPT_SUGGESTIONS.map((item, sIdx) => (
              <button
                key={sIdx}
                type="button"
                className="suggestion-chip"
                onClick={() => handleSendMessage(item.prompt)}
              >
                <span className="suggestion-category">{item.category}</span>
                <span className="suggestion-text">{item.prompt}</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Message Input Bar */}
      <div className="chat-input-container">
        <form
          className="chat-input-form"
          onSubmit={(e) => {
            e.preventDefault()
            handleSendMessage()
          }}
        >
          <textarea
            ref={textareaRef}
            className="chat-textarea"
            rows="2"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={`Ask anything about algorithms, patterns, LeetCode problems in ${language.toUpperCase()}... (Shift+Enter for newline)`}
            disabled={loading}
          />
          <button
            type="submit"
            className="chat-send-btn"
            disabled={!input.trim() || loading}
            aria-label="Send Message"
          >
            <Send size={16} />
          </button>
        </form>
        <div className="chat-footer-hint">
          <span>AlgoMentor AI Agentic RAG • LangGraph • Multi-Language Support ({language.toUpperCase()}) • Verified Knowledge Base</span>
        </div>
      </div>

      {/* Settings Modal */}
      {showSettings && (
        <div className="modal-overlay" onClick={() => setShowSettings(false)}>
          <div className="modal-card" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>AI Engine Settings</h3>
              <button type="button" className="close-btn" onClick={() => setShowSettings(false)}>✕</button>
            </div>

            <div className="modal-body">
              <div className="form-group">
                <label>AI Provider</label>
                <select
                  value={provider}
                  onChange={(e) => setProvider(e.target.value)}
                  className="modal-select"
                >
                  <option value="ollama">Local Ollama (Llama 3.2 - Recommended Offline)</option>
                  <option value="gemini">Google Gemini 1.5 Flash (Ultra-fast Cloud)</option>
                  <option value="groq">Groq Llama 3.3 70B (Fast Cloud)</option>
                  <option value="openai">OpenAI GPT-4o-mini (Cloud)</option>
                </select>
              </div>

              {provider === 'ollama' ? (
                <div className="form-group">
                  <label>Ollama Model Name</label>
                  <input
                    type="text"
                    value={ollamaModel}
                    onChange={(e) => setOllamaModel(e.target.value)}
                    placeholder="llama3.2"
                    className="modal-input"
                  />
                  <p className="form-hint">Make sure `ollama run llama3.2` is running locally.</p>
                </div>
              ) : (
                <div className="form-group">
                  <label>{provider.toUpperCase()} API Key</label>
                  <input
                    type="password"
                    value={apiKey}
                    onChange={(e) => setApiKey(e.target.value)}
                    placeholder={`Enter your ${provider} API key...`}
                    className="modal-input"
                  />
                  <p className="form-hint">Your key is stored securely only in your browser local storage.</p>
                </div>
              )}
            </div>

            <div className="modal-footer">
              <button type="button" className="secondary-btn" onClick={() => setShowSettings(false)}>Cancel</button>
              <button type="button" className="primary-btn" onClick={handleSaveSettings}>Save Settings</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
