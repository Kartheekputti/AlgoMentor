import { useState, useEffect, useRef } from 'react'
import {
  FileText,
  Plus,
  Search,
  Pin,
  Star,
  Lock,
  Unlock,
  Trash2,
  Copy,
  Download,
  Printer,
  Edit3,
  PenTool,
  Image as ImageIcon,
  Mic,
  MicOff,
  Volume2,
  CheckSquare,
  Square,
  List,
  ListOrdered,
  AlignLeft,
  AlignCenter,
  AlignRight,
  Bold,
  Italic,
  Underline,
  Strikethrough,
  Highlighter,
  Palette,
  RotateCcw,
  RotateCw,
  Folder,
  Tag,
  Grid,
  Menu,
  Check,
  ChevronLeft,
  Share2,
  Eraser
} from 'lucide-react'

const FOLDERS = [
  { id: 'all', label: 'All Notes' },
  { id: 'patterns', label: 'DSA Patterns' },
  { id: 'solutions', label: 'LeetCode Solutions' },
  { id: 'interviews', label: 'Interview Prep' },
  { id: 'system-design', label: 'System Design' },
  { id: 'quick', label: 'Quick Notes' },
]

const PAPER_TEMPLATES = [
  { id: 'blank', label: 'Blank' },
  { id: 'ruled', label: 'Ruled Lines' },
  { id: 'grid', label: 'Graph Grid' },
  { id: 'dots', label: 'Dot Grid' },
]

const PAPER_THEMES = [
  { id: 'dark-slate', label: 'Dark Slate', bg: '#0e1626', text: '#f1f5f9', border: 'rgba(255,255,255,0.08)' },
  { id: 'amoled', label: 'AMOLED Black', bg: '#09090b', text: '#f8fafc', border: 'rgba(255,255,255,0.1)' },
  { id: 'sepia', label: 'Warm Ivory', bg: '#fbf8f2', text: '#1e293b', border: 'rgba(0,0,0,0.1)' },
  { id: 'white', label: 'Clean White', bg: '#ffffff', text: '#0f172a', border: 'rgba(0,0,0,0.12)' },
]

const HIGHLIGHT_COLORS = [
  { name: 'Yellow', color: 'rgba(254, 240, 138, 0.45)' },
  { name: 'Green', color: 'rgba(187, 247, 208, 0.45)' },
  { name: 'Pink', color: 'rgba(254, 205, 211, 0.45)' },
  { name: 'Blue', color: 'rgba(186, 230, 253, 0.45)' },
  { name: 'Purple', color: 'rgba(233, 213, 255, 0.45)' },
]

const TEXT_COLORS = [
  '#f8fafc', '#94a3b8', '#38bdf8', '#34d399', '#fbbf24', '#f87171', '#c084fc', '#0f172a'
]

const S_PEN_TOOLS = [
  { id: 'pen', label: 'Ballpoint Pen', size: 3 },
  { id: 'calligraphy', label: 'Calligraphy', size: 6 },
  { id: 'highlighter', label: 'Highlighter', size: 16, opacity: 0.35 },
  { id: 'pencil', label: 'Pencil', size: 2, opacity: 0.7 },
  { id: 'eraser', label: 'Eraser', size: 20 },
]

export default function SamsungNotes({
  notes = [],
  activeNoteId = null,
  onSelectNote,
  onSaveNote,
  onDeleteNote,
  onDuplicateNote,
  loggedUser
}) {
  const [activeFolder, setActiveFolder] = useState('all')
  const [searchQuery, setSearchQuery] = useState('')
  const [viewMode, setViewMode] = useState('grid') // 'grid' | 'list'
  const [activeNote, setActiveNote] = useState(null)
  const [editorMode, setEditorMode] = useState('text') // 'text' | 'spen'
  const [paperTemplate, setPaperTemplate] = useState('grid')
  const [paperTheme, setPaperTheme] = useState('dark-slate')
  const [saveStatus, setSaveStatus] = useState('All changes saved')

  // Note fields
  const [title, setTitle] = useState('Untitled Note')
  const [folder, setFolder] = useState('patterns')
  const [tags, setTags] = useState([])
  const [tagInput, setTagInput] = useState('')
  const [isPinned, setIsPinned] = useState(false)
  const [isLocked, setIsLocked] = useState(false)
  const [lockPin, setLockPin] = useState('')
  const [isUnlockedForViewing, setIsUnlockedForViewing] = useState(false)
  const [pinModalOpen, setPinModalOpen] = useState(false)
  const [pinAttempt, setPinAttempt] = useState('')
  const [pinError, setPinError] = useState('')

  // S-Pen drawing canvas state
  const [selectedTool, setSelectedTool] = useState('pen')
  const [penColor, setPenColor] = useState('#60a5fa')
  const [penSize, setPenSize] = useState(3)
  const [isDrawing, setIsDrawing] = useState(false)
  const canvasRef = useRef(null)
  const canvasHistoryRef = useRef([])

  // Audio Voice Memo state
  const [isRecording, setIsRecording] = useState(false)
  const [recordingTime, setRecordingTime] = useState(0)
  const [audioUrl, setAudioUrl] = useState(null)
  const mediaRecorderRef = useRef(null)
  const audioChunksRef = useRef([])
  const timerIntervalRef = useRef(null)

  // Rich Text Editor Ref
  const editorRef = useRef(null)

  // Load selected or first note
  useEffect(() => {
    if (activeNoteId) {
      const found = notes.find((n) => n.id === activeNoteId)
      if (found) {
        loadNoteIntoState(found)
        return
      }
    }
    if (notes.length > 0 && !activeNote) {
      loadNoteIntoState(notes[0])
    } else if (notes.length === 0 && !activeNote) {
      handleCreateNewNote()
    }
  }, [activeNoteId, notes])

  const loadNoteIntoState = (note) => {
    setActiveNote(note)
    setTitle(note.title || 'Untitled Note')
    setFolder(note.folder || 'patterns')
    setTags(note.tags || [])
    setIsPinned(Boolean(note.isPinned))
    setIsLocked(Boolean(note.isLocked))
    setLockPin(note.lockPin || '')
    setPaperTemplate(note.paperTemplate || 'grid')
    setPaperTheme(note.paperTheme || 'dark-slate')
    setAudioUrl(note.audioUrl || null)
    setIsUnlockedForViewing(!note.isLocked)

    if (editorRef.current) {
      editorRef.current.innerHTML = note.content || ''
    }
  }

  // Auto-sync content into editor when note changes
  useEffect(() => {
    if (editorRef.current && activeNote && !activeNote.isLocked) {
      if (editorRef.current.innerHTML !== activeNote.content) {
        editorRef.current.innerHTML = activeNote.content || ''
      }
    }
  }, [activeNote?.id])

  const executeEditorCommand = (command, value = null) => {
    if (!editorRef.current) return
    editorRef.current.focus()
    document.execCommand(command, false, value)
    triggerAutoSave()
  }

  const handleApplyHighlight = (color) => {
    if (!editorRef.current) return
    editorRef.current.focus()
    document.execCommand('hiliteColor', false, color)
    triggerAutoSave()
  }

  const handleInsertChecklist = () => {
    if (!editorRef.current) return
    editorRef.current.focus()
    const checklistHtml = `
      <div class="samsung-checklist-item" style="display:flex; align-items:center; gap:8px; margin: 6px 0;">
        <input type="checkbox" class="checklist-box" style="width:18px; height:18px; cursor:pointer; accent-color:#6366f1;" />
        <span class="checklist-label" style="outline:none;" contenteditable="true">Task item...</span>
      </div>
    `
    document.execCommand('insertHTML', false, checklistHtml)
    triggerAutoSave()
  }

  const handleInsertImage = (e) => {
    const file = e.target.files?.[0]
    if (!file || !editorRef.current) return
    const reader = new FileReader()
    reader.onload = () => {
      editorRef.current.focus()
      const imgTag = `<img src="${reader.result}" alt="Note diagram" style="max-width:100%; border-radius:12px; margin:12px 0; box-shadow:0 8px 24px rgba(0,0,0,0.25);" />`
      document.execCommand('insertHTML', false, imgTag)
      triggerAutoSave()
    }
    reader.readAsDataURL(file)
    e.target.value = ''
  }

  // Voice memo recording using Web Audio API
  const toggleRecording = async () => {
    if (isRecording) {
      // Stop recording
      if (mediaRecorderRef.current) {
        mediaRecorderRef.current.stop()
      }
      setIsRecording(false)
      clearInterval(timerIntervalRef.current)
    } else {
      // Start recording
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
        mediaRecorderRef.current = new MediaRecorder(stream)
        audioChunksRef.current = []

        mediaRecorderRef.current.ondataavailable = (event) => {
          if (event.data.size > 0) {
            audioChunksRef.current.push(event.data)
          }
        }

        mediaRecorderRef.current.onstop = () => {
          const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' })
          const url = URL.createObjectURL(audioBlob)
          setAudioUrl(url)
          triggerAutoSave({ audioUrl: url })
          stream.getTracks().forEach((track) => track.stop())
        }

        mediaRecorderRef.current.start()
        setIsRecording(true)
        setRecordingTime(0)
        timerIntervalRef.current = setInterval(() => {
          setRecordingTime((prev) => prev + 1)
        }, 1000)
      } catch (err) {
        alert('Microphone access denied or not available.')
      }
    }
  }

  // S-Pen Drawing Canvas logic
  useEffect(() => {
    if (editorMode === 'spen' && canvasRef.current) {
      const canvas = canvasRef.current
      const ctx = canvas.getContext('2d')
      // Set resolution based on element size
      canvas.width = canvas.parentElement.clientWidth || 800
      canvas.height = 500
      ctx.lineCap = 'round'
      ctx.lineJoin = 'round'
    }
  }, [editorMode])

  const startDrawing = (e) => {
    if (editorMode !== 'spen' || !canvasRef.current) return
    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    const rect = canvas.getBoundingClientRect()
    const x = e.clientX - rect.left
    const y = e.clientY - rect.top

    ctx.beginPath()
    ctx.moveTo(x, y)
    setIsDrawing(true)

    // Tool styling
    if (selectedTool === 'eraser') {
      ctx.globalCompositeOperation = 'destination-out'
      ctx.lineWidth = penSize * 3
    } else if (selectedTool === 'highlighter') {
      ctx.globalCompositeOperation = 'source-over'
      ctx.strokeStyle = penColor
      ctx.globalAlpha = 0.35
      ctx.lineWidth = penSize * 4
    } else {
      ctx.globalCompositeOperation = 'source-over'
      ctx.strokeStyle = penColor
      ctx.globalAlpha = 1.0
      ctx.lineWidth = penSize
    }
  }

  const draw = (e) => {
    if (!isDrawing || !canvasRef.current) return
    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    const rect = canvas.getBoundingClientRect()
    const x = e.clientX - rect.left
    const y = e.clientY - rect.top
    ctx.lineTo(x, y)
    ctx.stroke()
  }

  const stopDrawing = () => {
    if (!isDrawing || !canvasRef.current) return
    setIsDrawing(false)
    const canvas = canvasRef.current
    canvasHistoryRef.current.push(canvas.toDataURL())
  }

  const clearCanvas = () => {
    if (!canvasRef.current) return
    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    canvasHistoryRef.current = []
  }

  const handleEmbedDrawingIntoNote = () => {
    if (!canvasRef.current || !editorRef.current) return
    const dataUrl = canvasRef.current.toDataURL()
    setEditorMode('text')
    setTimeout(() => {
      if (editorRef.current) {
        editorRef.current.focus()
        const imgTag = `<img src="${dataUrl}" alt="S-Pen Sketch" style="max-width:100%; border-radius:12px; margin:12px 0; border:1px solid rgba(255,255,255,0.15);" />`
        document.execCommand('insertHTML', false, imgTag)
        triggerAutoSave()
      }
    }, 100)
  }

  // Auto-save logic
  const triggerAutoSave = (overrides = {}) => {
    setSaveStatus('Saving...')
    const content = editorRef.current ? editorRef.current.innerHTML : activeNote?.content || ''
    const updatedNote = {
      id: activeNote?.id || `note-${Date.now()}`,
      title: overrides.title !== undefined ? overrides.title : title,
      content: overrides.content !== undefined ? overrides.content : content,
      folder: overrides.folder !== undefined ? overrides.folder : folder,
      tags: overrides.tags !== undefined ? overrides.tags : tags,
      isPinned: overrides.isPinned !== undefined ? overrides.isPinned : isPinned,
      isLocked: overrides.isLocked !== undefined ? overrides.isLocked : isLocked,
      lockPin: overrides.lockPin !== undefined ? overrides.lockPin : lockPin,
      paperTemplate: overrides.paperTemplate !== undefined ? overrides.paperTemplate : paperTemplate,
      paperTheme: overrides.paperTheme !== undefined ? overrides.paperTheme : paperTheme,
      audioUrl: overrides.audioUrl !== undefined ? overrides.audioUrl : audioUrl,
      updatedAt: new Date().toISOString(),
    }

    onSaveNote(updatedNote)
    setActiveNote(updatedNote)
    setTimeout(() => setSaveStatus('All changes saved'), 600)
  }

  const handleCreateNewNote = (templateType = 'blank') => {
    let initialContent = ''
    let initialTitle = 'Untitled Note'
    let initialFolder = 'patterns'

    if (templateType === 'dsa') {
      initialTitle = 'Algorithm Pattern: '
      initialContent = `
        <h2>Problem Statement</h2>
        <p>Write problem description, constraints, and target time/space complexity here.</p>
        <h2>Intuition & Key Observation</h2>
        <p>Why does this approach work? (e.g. Monotonic property, overlapping subproblems)</p>
        <h2>Step-by-Step Approach</h2>
        <ul>
          <li>Step 1: Initialize pointers / data structure</li>
          <li>Step 2: Traverse and update condition</li>
          <li>Step 3: Return result</li>
        </ul>
        <h2>Complexity Analysis</h2>
        <p><strong>Time Complexity:</strong> O(N)<br><strong>Space Complexity:</strong> O(1)</p>
      `
    } else if (templateType === 'checklist') {
      initialTitle = 'DSA Prep Checklist'
      initialContent = `
        <h2>Daily Goals</h2>
        <div class="samsung-checklist-item" style="display:flex; align-items:center; gap:8px; margin: 6px 0;">
          <input type="checkbox" class="checklist-box" style="width:18px; height:18px; accent-color:#6366f1;" />
          <span contenteditable="true">Solve 2 Striver A-Z Sheet problems</span>
        </div>
        <div class="samsung-checklist-item" style="display:flex; align-items:center; gap:8px; margin: 6px 0;">
          <input type="checkbox" class="checklist-box" style="width:18px; height:18px; accent-color:#6366f1;" />
          <span contenteditable="true">Revise sliding window & two-pointers</span>
        </div>
        <div class="samsung-checklist-item" style="display:flex; align-items:center; gap:8px; margin: 6px 0;">
          <input type="checkbox" class="checklist-box" style="width:18px; height:18px; accent-color:#6366f1;" />
          <span contenteditable="true">Review time complexity of graph algorithms</span>
        </div>
      `
    }

    const newNote = {
      id: `note-${Date.now()}`,
      title: initialTitle,
      content: initialContent,
      folder: initialFolder,
      tags: ['#dsa'],
      isPinned: false,
      isLocked: false,
      paperTemplate: 'grid',
      paperTheme: 'dark-slate',
      updatedAt: new Date().toISOString(),
    }

    onSaveNote(newNote)
    loadNoteIntoState(newNote)
    if (onSelectNote) onSelectNote(newNote.id)
  }

  // Add & remove tags
  const handleAddTag = (e) => {
    if (e.key === 'Enter' && tagInput.trim()) {
      e.preventDefault()
      let formatted = tagInput.trim()
      if (!formatted.startsWith('#')) formatted = `#${formatted}`
      if (!tags.includes(formatted)) {
        const nextTags = [...tags, formatted]
        setTags(nextTags)
        triggerAutoSave({ tags: nextTags })
      }
      setTagInput('')
    }
  }

  const handleRemoveTag = (t) => {
    const nextTags = tags.filter((x) => x !== t)
    setTags(nextTags)
    triggerAutoSave({ tags: nextTags })
  }

  // Lock note pin verification
  const handleUnlockAttempt = () => {
    if (pinAttempt === lockPin) {
      setIsUnlockedForViewing(true)
      setPinModalOpen(false)
      setPinAttempt('')
      setPinError('')
      if (editorRef.current) {
        editorRef.current.innerHTML = activeNote?.content || ''
      }
    } else {
      setPinError('Incorrect 4-digit PIN.')
    }
  }

  const handleSetLockPin = () => {
    const entered = window.prompt('Set a 4-digit PIN to protect this note:', '1234')
    if (entered && entered.trim().length >= 4) {
      const pinVal = entered.trim()
      setLockPin(pinVal)
      setIsLocked(true)
      setIsUnlockedForViewing(true)
      triggerAutoSave({ isLocked: true, lockPin: pinVal })
    }
  }

  // Export handlers
  const handleExport = (format) => {
    if (!activeNote) return
    let blob = null
    let filename = `${activeNote.title || 'note'}.${format}`

    if (format === 'txt') {
      const text = editorRef.current ? editorRef.current.innerText : activeNote.content
      blob = new Blob([text], { type: 'text/plain;charset=utf-8' })
    } else if (format === 'md') {
      const text = editorRef.current ? editorRef.current.innerText : activeNote.content
      const mdContent = `# ${activeNote.title}\n\nFolder: ${activeNote.folder}\nTags: ${activeNote.tags?.join(' ')}\n\n${text}`
      blob = new Blob([mdContent], { type: 'text/markdown;charset=utf-8' })
    } else if (format === 'html') {
      const htmlContent = `<!DOCTYPE html><html><head><title>${activeNote.title}</title><style>body{font-family:sans-serif;padding:2rem;line-height:1.6;}</style></head><body><h1>${activeNote.title}</h1>${editorRef.current ? editorRef.current.innerHTML : activeNote.content}</body></html>`
      blob = new Blob([htmlContent], { type: 'text/html;charset=utf-8' })
    } else if (format === 'pdf') {
      window.print()
      return
    }

    if (blob) {
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = filename
      a.click()
      URL.revokeObjectURL(url)
    }
  }

  // Filter notes
  const filteredNotes = notes.filter((n) => {
    const matchesFolder = activeFolder === 'all' || n.folder === activeFolder
    const matchesSearch =
      !searchQuery ||
      n.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (n.content && n.content.toLowerCase().includes(searchQuery.toLowerCase())) ||
      (n.tags && n.tags.some((t) => t.toLowerCase().includes(searchQuery.toLowerCase())))
    return matchesFolder && matchesSearch
  }).sort((a, b) => {
    if (a.isPinned && !b.isPinned) return -1
    if (!a.isPinned && b.isPinned) return 1
    return new Date(b.updatedAt || 0) - new Date(a.updatedAt || 0)
  })

  const currentTheme = PAPER_THEMES.find((t) => t.id === paperTheme) || PAPER_THEMES[0]

  return (
    <div className="samsung-notes-wrapper">
      {/* LEFT DRAWER / NOTE LIST */}
      <div className="snotes-sidebar">
        <div className="snotes-sidebar-header">
          <div className="snotes-brand">
            <Edit3 size={18} className="text-indigo-400" />
            <span>Samsung Notes</span>
          </div>
          <div className="snotes-header-tools">
            <button
              type="button"
              className="snotes-icon-btn"
              title={viewMode === 'grid' ? 'Switch to List view' : 'Switch to Card view'}
              onClick={() => setViewMode(viewMode === 'grid' ? 'list' : 'grid')}
            >
              <Grid size={16} />
            </button>
            <button
              type="button"
              className="snotes-primary-add-btn"
              title="Create new note"
              onClick={() => handleCreateNewNote('blank')}
            >
              <Plus size={16} />
              <span>New</span>
            </button>
          </div>
        </div>

        {/* Search */}
        <div className="snotes-search-bar">
          <Search size={15} className="text-slate-400" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search notes, tags, code..."
          />
        </div>

        {/* Folders Tab Strip */}
        <div className="snotes-folders-scroll">
          {FOLDERS.map((f) => (
            <button
              key={f.id}
              type="button"
              className={`snotes-folder-chip ${activeFolder === f.id ? 'active' : ''}`}
              onClick={() => setActiveFolder(f.id)}
            >
              {f.label}
            </button>
          ))}
        </div>

        {/* Quick Templates Strip */}
        <div className="snotes-template-bar">
          <span className="template-label">Templates:</span>
          <button type="button" onClick={() => handleCreateNewNote('dsa')}>+ DSA Problem</button>
          <button type="button" onClick={() => handleCreateNewNote('checklist')}>+ Checklist</button>
        </div>

        {/* Notes List */}
        <div className={`snotes-list-scroll ${viewMode}`}>
          {filteredNotes.length === 0 ? (
            <div className="snotes-empty">
              <FileText size={32} className="text-slate-500" />
              <p>No notes found in this category.</p>
              <button type="button" className="snotes-btn-link" onClick={() => handleCreateNewNote('blank')}>
                Create your first note
              </button>
            </div>
          ) : (
            filteredNotes.map((n) => {
              const isSelected = activeNote?.id === n.id
              const snippet = n.content ? n.content.replace(/<[^>]*>?/gm, '').slice(0, 90) : 'No content'

              return (
                <div
                  key={n.id}
                  className={`snotes-card ${isSelected ? 'active' : ''}`}
                  onClick={() => {
                    if (n.isLocked) {
                      setActiveNote(n)
                      setPinModalOpen(true)
                    } else {
                      loadNoteIntoState(n)
                      if (onSelectNote) onSelectNote(n.id)
                    }
                  }}
                >
                  <div className="snotes-card-top">
                    <div className="snotes-card-title-row">
                      {n.isPinned && <Pin size={13} className="text-amber-400 pin-badge" />}
                      {n.isLocked && <Lock size={13} className="text-rose-400 lock-badge" />}
                      <h4 className="snotes-card-title">{n.title || 'Untitled Note'}</h4>
                    </div>
                    <span className="snotes-card-folder">{n.folder}</span>
                  </div>

                  <p className="snotes-card-snippet">
                    {n.isLocked ? '🔒 Protected note (PIN required)' : snippet}
                  </p>

                  <div className="snotes-card-footer">
                    <div className="snotes-card-tags">
                      {n.tags?.slice(0, 2).map((t, idx) => (
                        <span key={idx} className="card-tag">{t}</span>
                      ))}
                    </div>
                    <span className="snotes-card-date">
                      {new Date(n.updatedAt || Date.now()).toLocaleDateString([], { month: 'short', day: 'numeric' })}
                    </span>
                  </div>
                </div>
              )
            })
          )}
        </div>
      </div>

      {/* RIGHT MAIN EDITOR */}
      <div className="snotes-editor-main">
        {/* Top Control Bar */}
        <div className="snotes-top-bar">
          <div className="snotes-top-meta">
            <span className="snotes-save-pill">{saveStatus}</span>
            {isPinned && <span className="snotes-pinned-pill">Pinned to Top</span>}
            {isLocked && <span className="snotes-locked-pill">PIN Protected</span>}
          </div>

          <div className="snotes-top-actions">
            {/* Template Selector */}
            <select
              className="snotes-select"
              value={paperTemplate}
              onChange={(e) => {
                setPaperTemplate(e.target.value)
                triggerAutoSave({ paperTemplate: e.target.value })
              }}
              title="Page Template"
            >
              {PAPER_TEMPLATES.map((p) => (
                <option key={p.id} value={p.id}>{p.label}</option>
              ))}
            </select>

            {/* Paper Theme */}
            <select
              className="snotes-select"
              value={paperTheme}
              onChange={(e) => {
                setPaperTheme(e.target.value)
                triggerAutoSave({ paperTheme: e.target.value })
              }}
              title="Paper Theme"
            >
              {PAPER_THEMES.map((th) => (
                <option key={th.id} value={th.id}>{th.label}</option>
              ))}
            </select>

            {/* Mode Switcher: Text vs S-Pen */}
            <div className="snotes-mode-toggle">
              <button
                type="button"
                className={`mode-toggle-btn ${editorMode === 'text' ? 'active' : ''}`}
                onClick={() => setEditorMode('text')}
                title="Rich Text Mode"
              >
                <Edit3 size={15} />
                <span>Text</span>
              </button>
              <button
                type="button"
                className={`mode-toggle-btn ${editorMode === 'spen' ? 'active' : ''}`}
                onClick={() => setEditorMode('spen')}
                title="S-Pen Sketch Canvas Mode"
              >
                <PenTool size={15} />
                <span>S-Pen Canvas</span>
              </button>
            </div>

            {/* Pin Toggle */}
            <button
              type="button"
              className={`snotes-tool-btn ${isPinned ? 'active' : ''}`}
              title="Pin to Top"
              onClick={() => {
                const nextVal = !isPinned
                setIsPinned(nextVal)
                triggerAutoSave({ isPinned: nextVal })
              }}
            >
              <Pin size={15} />
            </button>

            {/* Lock Toggle */}
            <button
              type="button"
              className={`snotes-tool-btn ${isLocked ? 'active' : ''}`}
              title={isLocked ? 'Unlock / change PIN' : 'Protect with PIN'}
              onClick={() => {
                if (isLocked) {
                  if (window.confirm('Remove PIN lock from this note?')) {
                    setIsLocked(false)
                    setLockPin('')
                    triggerAutoSave({ isLocked: false, lockPin: '' })
                  }
                } else {
                  handleSetLockPin()
                }
              }}
            >
              {isLocked ? <Lock size={15} className="text-rose-400" /> : <Unlock size={15} />}
            </button>

            {/* Export Dropdown */}
            <div className="snotes-export-dropdown">
              <button type="button" className="snotes-tool-btn" title="Export Note">
                <Download size={15} />
              </button>
              <div className="export-menu">
                <button type="button" onClick={() => handleExport('md')}>Markdown (.md)</button>
                <button type="button" onClick={() => handleExport('txt')}>Plain Text (.txt)</button>
                <button type="button" onClick={() => handleExport('html')}>HTML (.html)</button>
                <button type="button" onClick={() => handleExport('pdf')}>Print / PDF</button>
              </div>
            </div>

            {/* Delete */}
            <button
              type="button"
              className="snotes-tool-btn delete"
              title="Delete Note"
              onClick={() => {
                if (window.confirm('Delete this note permanently?')) {
                  onDeleteNote(activeNote?.id)
                }
              }}
            >
              <Trash2 size={15} />
            </button>
          </div>
        </div>

        {/* Note Metadata Inputs: Title, Folder, Tags */}
        <div className="snotes-meta-bar">
          <input
            type="text"
            className="snotes-title-input"
            value={title}
            onChange={(e) => {
              setTitle(e.target.value)
              triggerAutoSave({ title: e.target.value })
            }}
            placeholder="Title of note..."
          />

          <div className="snotes-meta-row">
            <div className="snotes-folder-select-wrap">
              <Folder size={14} className="text-slate-400" />
              <select
                value={folder}
                onChange={(e) => {
                  setFolder(e.target.value)
                  triggerAutoSave({ folder: e.target.value })
                }}
                className="snotes-inline-select"
              >
                {FOLDERS.filter((f) => f.id !== 'all').map((f) => (
                  <option key={f.id} value={f.id}>{f.label}</option>
                ))}
              </select>
            </div>

            <div className="snotes-tags-wrap">
              <Tag size={14} className="text-slate-400" />
              <div className="snotes-tags-list">
                {tags.map((t, idx) => (
                  <span key={idx} className="snotes-tag-chip">
                    {t}
                    <button type="button" onClick={() => handleRemoveTag(t)}>×</button>
                  </span>
                ))}
                <input
                  type="text"
                  value={tagInput}
                  onChange={(e) => setTagInput(e.target.value)}
                  onKeyDown={handleAddTag}
                  placeholder="Add #tag (Enter)"
                  className="snotes-tag-input"
                />
              </div>
            </div>
          </div>
        </div>

        {/* S-PEN DRAWING TOOLBAR (When in S-Pen mode) */}
        {editorMode === 'spen' && (
          <div className="spen-toolbar">
            <div className="spen-tools-group">
              {S_PEN_TOOLS.map((tool) => (
                <button
                  key={tool.id}
                  type="button"
                  className={`spen-tool-btn ${selectedTool === tool.id ? 'active' : ''}`}
                  onClick={() => {
                    setSelectedTool(tool.id)
                    setPenSize(tool.size)
                  }}
                >
                  {tool.id === 'eraser' ? <Eraser size={16} /> : <PenTool size={16} />}
                  <span>{tool.label}</span>
                </button>
              ))}
            </div>

            <div className="spen-color-group">
              {TEXT_COLORS.map((c, idx) => (
                <button
                  key={idx}
                  type="button"
                  className={`spen-color-circle ${penColor === c ? 'active' : ''}`}
                  style={{ backgroundColor: c }}
                  onClick={() => setPenColor(c)}
                />
              ))}
              <input
                type="color"
                value={penColor}
                onChange={(e) => setPenColor(e.target.value)}
                className="spen-color-picker"
                title="Custom color"
              />
            </div>

            <div className="spen-slider-group">
              <span className="slider-label">Width:</span>
              <input
                type="range"
                min="1"
                max="30"
                value={penSize}
                onChange={(e) => setPenSize(Number(e.target.value))}
                className="spen-range"
              />
            </div>

            <div className="spen-actions-group">
              <button type="button" className="spen-btn" onClick={clearCanvas}>Clear</button>
              <button type="button" className="spen-btn primary" onClick={handleEmbedDrawingIntoNote}>
                Insert Sketch into Note
              </button>
            </div>
          </div>
        )}

        {/* RICH TEXT FORMATTING TOOLBAR (When in Text Mode) */}
        {editorMode === 'text' && (
          <div className="snotes-rich-toolbar">
            <button type="button" onClick={() => executeEditorCommand('formatBlock', '<h1>')} title="Heading 1"><b>H1</b></button>
            <button type="button" onClick={() => executeEditorCommand('formatBlock', '<h2>')} title="Heading 2"><b>H2</b></button>
            <button type="button" onClick={() => executeEditorCommand('formatBlock', '<p>')} title="Paragraph">P</button>

            <div className="toolbar-divider" />

            <button type="button" onClick={() => executeEditorCommand('bold')} title="Bold">
              <Bold size={15} />
            </button>
            <button type="button" onClick={() => executeEditorCommand('italic')} title="Italic">
              <Italic size={15} />
            </button>
            <button type="button" onClick={() => executeEditorCommand('underline')} title="Underline">
              <Underline size={15} />
            </button>
            <button type="button" onClick={() => executeEditorCommand('strikeThrough')} title="Strikethrough">
              <Strikethrough size={15} />
            </button>

            <div className="toolbar-divider" />

            {/* Samsung Highlighter Dropdown */}
            <div className="highlighter-group">
              <button type="button" className="highlighter-icon" title="Highlighter Pen">
                <Highlighter size={15} />
              </button>
              <div className="highlighter-palette">
                {HIGHLIGHT_COLORS.map((h, idx) => (
                  <button
                    key={idx}
                    type="button"
                    style={{ backgroundColor: h.color }}
                    className="highlight-dot"
                    title={`${h.name} Highlighter`}
                    onClick={() => handleApplyHighlight(h.color)}
                  />
                ))}
              </div>
            </div>

            {/* Text Color Picker */}
            <div className="color-palette-group">
              <Palette size={15} className="text-slate-400" />
              {TEXT_COLORS.slice(0, 6).map((c, idx) => (
                <button
                  key={idx}
                  type="button"
                  className="color-dot"
                  style={{ backgroundColor: c }}
                  onClick={() => executeEditorCommand('foreColor', c)}
                />
              ))}
            </div>

            <div className="toolbar-divider" />

            {/* Alignments */}
            <button type="button" onClick={() => executeEditorCommand('justifyLeft')} title="Align Left">
              <AlignLeft size={15} />
            </button>
            <button type="button" onClick={() => executeEditorCommand('justifyCenter')} title="Align Center">
              <AlignCenter size={15} />
            </button>
            <button type="button" onClick={() => executeEditorCommand('justifyRight')} title="Align Right">
              <AlignRight size={15} />
            </button>

            <div className="toolbar-divider" />

            {/* Lists & Checklist */}
            <button type="button" onClick={() => executeEditorCommand('insertUnorderedList')} title="Bullet List">
              <List size={15} />
            </button>
            <button type="button" onClick={() => executeEditorCommand('insertOrderedList')} title="Numbered List">
              <ListOrdered size={15} />
            </button>
            <button type="button" className="checklist-btn" onClick={handleInsertChecklist} title="Interactive Checklist">
              <CheckSquare size={15} />
              <span>Checklist</span>
            </button>

            <div className="toolbar-divider" />

            {/* Image Upload */}
            <label className="image-upload-label" title="Insert Image from Device">
              <ImageIcon size={15} />
              <span>Image</span>
              <input type="file" accept="image/*" onChange={handleInsertImage} />
            </label>

            {/* Voice Memo Recording */}
            <button
              type="button"
              className={`voice-memo-btn ${isRecording ? 'recording' : ''}`}
              onClick={toggleRecording}
              title={isRecording ? 'Stop Recording' : 'Record Audio Memo'}
            >
              {isRecording ? <MicOff size={15} /> : <Mic size={15} />}
              <span>{isRecording ? `Recording (${recordingTime}s)...` : 'Voice Memo'}</span>
            </button>

            <div className="toolbar-divider" />

            {/* Undo / Redo */}
            <button type="button" onClick={() => executeEditorCommand('undo')} title="Undo">
              <RotateCcw size={15} />
            </button>
            <button type="button" onClick={() => executeEditorCommand('redo')} title="Redo">
              <RotateCw size={15} />
            </button>
          </div>
        )}

        {/* AUDIO MEMO PLAYER IF ATTACHED */}
        {audioUrl && (
          <div className="snotes-audio-player">
            <Volume2 size={16} className="text-indigo-400" />
            <span className="audio-label">Attached Voice Memo:</span>
            <audio src={audioUrl} controls className="audio-element" />
            <button
              type="button"
              className="remove-audio-btn"
              title="Remove audio memo"
              onClick={() => {
                setAudioUrl(null)
                triggerAutoSave({ audioUrl: null })
              }}
            >
              ✕
            </button>
          </div>
        )}

        {/* EDITOR AREA: LOCKED OR UNLOCKED */}
        {isLocked && !isUnlockedForViewing ? (
          <div className="locked-note-view">
            <Lock size={48} className="text-rose-400" />
            <h3>This note is locked</h3>
            <p>Enter the 4-digit PIN to view and edit this note.</p>
            <button
              type="button"
              className="snotes-unlock-btn"
              onClick={() => setPinModalOpen(true)}
            >
              Unlock Note
            </button>
          </div>
        ) : (
          <div className="editor-paper-container">
            {editorMode === 'text' ? (
              <div
                ref={editorRef}
                className={`snotes-paper-canvas template-${paperTemplate}`}
                style={{
                  backgroundColor: currentTheme.bg,
                  color: currentTheme.text,
                }}
                contentEditable
                suppressContentEditableWarning
                onInput={() => triggerAutoSave()}
                data-placeholder="Start writing notes, formulas, checklists, or DSA solutions..."
              />
            ) : (
              <div
                className={`snotes-canvas-wrap template-${paperTemplate}`}
                style={{ backgroundColor: currentTheme.bg }}
              >
                <canvas
                  ref={canvasRef}
                  className="spen-canvas"
                  onMouseDown={startDrawing}
                  onMouseMove={draw}
                  onMouseUp={stopDrawing}
                  onMouseLeave={stopDrawing}
                />
              </div>
            )}
          </div>
        )}
      </div>

      {/* PIN UNLOCK MODAL */}
      {pinModalOpen && (
        <div className="modal-overlay" onClick={() => setPinModalOpen(false)}>
          <div className="modal-card mini" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Enter Note PIN</h3>
              <button type="button" className="close-btn" onClick={() => setPinModalOpen(false)}>✕</button>
            </div>
            <div className="modal-body">
              <p>Please enter the 4-digit security PIN for this note:</p>
              <input
                type="password"
                maxLength="6"
                value={pinAttempt}
                onChange={(e) => setPinAttempt(e.target.value)}
                placeholder="PIN"
                className="modal-input text-center text-xl tracking-widest"
                autoFocus
              />
              {pinError && <p className="error-text mt-2">{pinError}</p>}
            </div>
            <div className="modal-footer">
              <button type="button" className="secondary-btn" onClick={() => setPinModalOpen(false)}>Cancel</button>
              <button type="button" className="primary-btn" onClick={handleUnlockAttempt}>Unlock</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
