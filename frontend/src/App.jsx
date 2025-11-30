import { useState, useEffect } from 'react'
import { api } from './api'
import Sidebar from './components/Sidebar'
import ChatInterface from './components/ChatInterface'
import Auth from './components/Auth'
import { auth, logout } from './firebase'
import { onAuthStateChanged } from 'firebase/auth'

function App() {
  // State management
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [conversations, setConversations] = useState([])
  const [currentConversationId, setCurrentConversationId] = useState(null)
  const [currentConversation, setCurrentConversation] = useState(null)
  const [messageLoading, setMessageLoading] = useState(false)

  // Listen for auth state changes
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser)
      setLoading(false)
    })
    return () => unsubscribe()
  }, [])

  // Load conversations when user logs in
  useEffect(() => {
    if (user) {
      loadConversations()
    }
  }, [user])

  // Load current conversation when ID changes
  useEffect(() => {
    if (currentConversationId) {
      loadCurrentConversation()
    }
  }, [currentConversationId])

  /**
   * Load all conversations from backend.
   * 
   * Requirements: 8.4, 8.5
   */
  const loadConversations = async () => {
    if (!user) return
    try {
      const convos = await api.listConversations(user.uid)
      setConversations(convos)
    } catch (error) {
      console.error('Error loading conversations:', error)
    }
  }

  /**
   * Load current conversation details.
   */
  const loadCurrentConversation = async () => {
    if (!user) return
    try {
      const convo = await api.getConversation(currentConversationId, user.uid)
      setCurrentConversation(convo)
    } catch (error) {
      console.error('Error loading conversation:', error)
    }
  }

  /**
   * Create a new conversation.
   */
  const handleNewConversation = async () => {
    if (!user) return
    try {
      const newConvo = await api.createConversation(user.uid)
      setConversations([newConvo, ...conversations])
      setCurrentConversationId(newConvo.id)
    } catch (error) {
      console.error('Error creating conversation:', error)
    }
  }

  /**
   * Delete a conversation.
   */
  const handleDeleteConversation = async (conversationId) => {
    if (!user) return
    try {
      await api.deleteConversation(conversationId, user.uid)
      
      // Remove from list
      setConversations(conversations.filter(c => c.id !== conversationId))
      
      // If deleting current conversation, clear it
      if (conversationId === currentConversationId) {
        setCurrentConversationId(null)
        setCurrentConversation(null)
      }
    } catch (error) {
      console.error('Error deleting conversation:', error)
      alert('Failed to delete conversation')
    }
  }

  /**
   * Send a message with optimistic updates.
   * 
   * Requirements: 2.4
   */
  const handleSendMessage = async (content) => {
    if (!currentConversationId || !content.trim()) {
      return
    }

    setMessageLoading(true)

    // Optimistic update: add user message immediately
    const userMessage = {
      role: 'user',
      content: content
    }

    const optimisticAssistantMessage = {
      role: 'assistant',
      stage1: [],
      stage2: [],
      stage3: {},
      metadata: {},
      loading: {
        stage1: true,
        stage2: false,
        stage3: false
      }
    }

    setCurrentConversation(prev => ({
      ...prev,
      messages: [...(prev?.messages || []), userMessage, optimisticAssistantMessage]
    }))

    try {
      // Stream the response
      await api.sendMessageStream(
        currentConversationId,
        content,
        (eventType, eventData) => {
          handleStreamEvent(eventType, eventData)
        },
        user.uid
      )

      // Reload conversation list to update titles
      loadConversations()
    } catch (error) {
      console.error('Error sending message:', error)
      // TODO: Rollback optimistic update on error
    } finally {
      setMessageLoading(false)
    }
  }

  const handleLogout = async () => {
    try {
      await logout()
      setConversations([])
      setCurrentConversationId(null)
      setCurrentConversation(null)
    } catch (error) {
      console.error('Error logging out:', error)
    }
  }

  /**
   * Handle SSE events from the backend.
   */
  const handleStreamEvent = (eventType, eventData) => {
    setCurrentConversation(prev => {
      if (!prev || !prev.messages) return prev

      const messages = [...prev.messages]
      const lastMessage = messages[messages.length - 1]

      if (lastMessage.role !== 'assistant') return prev

      const updatedMessage = { ...lastMessage }

      switch (eventType) {
        case 'stage1_start':
          updatedMessage.loading = { stage1: true, stage2: false, stage3: false }
          break

        case 'stage1_complete':
          updatedMessage.stage1 = eventData
          updatedMessage.loading = { stage1: false, stage2: true, stage3: false }
          break

        case 'stage2_start':
          updatedMessage.loading = { stage1: false, stage2: true, stage3: false }
          break

        case 'stage2_complete':
          updatedMessage.stage2 = eventData.rankings
          updatedMessage.metadata = {
            label_to_model: eventData.label_to_model,
            aggregate_rankings: eventData.aggregate_rankings
          }
          updatedMessage.loading = { stage1: false, stage2: false, stage3: true }
          break

        case 'stage3_start':
          updatedMessage.loading = { stage1: false, stage2: false, stage3: true }
          break

        case 'stage3_complete':
          updatedMessage.stage3 = eventData
          updatedMessage.loading = { stage1: false, stage2: false, stage3: false }
          break

        case 'complete':
          updatedMessage.loading = { stage1: false, stage2: false, stage3: false }
          break

        case 'error':
          console.error('Stream error:', eventData)
          updatedMessage.error = eventData
          updatedMessage.loading = { stage1: false, stage2: false, stage3: false }
          break

        default:
          console.log('Unknown event type:', eventType)
      }

      messages[messages.length - 1] = updatedMessage
      return { ...prev, messages }
    })
  }

  // Show loading spinner while checking auth
  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  // Show auth screen if not logged in
  if (!user) {
    return <Auth />
  }

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <Sidebar
        conversations={conversations}
        currentConversationId={currentConversationId}
        onSelectConversation={setCurrentConversationId}
        onNewConversation={handleNewConversation}
        onDeleteConversation={handleDeleteConversation}
        userId={user.uid}
      />

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-white border-b border-gray-200 p-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-gray-900">
              Mirmer AI
            </h1>
            
            {/* User Info & Logout */}
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-3">
                <img 
                  src={user.photoURL} 
                  alt={user.displayName}
                  className="w-8 h-8 rounded-full"
                />
                <span className="text-sm text-gray-700">{user.displayName}</span>
              </div>
              <button
                onClick={handleLogout}
                className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
              >
                Logout
              </button>
            </div>
          </div>
        </div>

        {/* Chat Interface */}
        <ChatInterface
          conversation={currentConversation}
          onSendMessage={handleSendMessage}
          loading={messageLoading}
        />
      </div>
    </div>
  )
}

export default App
