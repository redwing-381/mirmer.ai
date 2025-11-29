import { useState, useEffect } from 'react'
import { api } from './api'

function App() {
  // State management
  const [conversations, setConversations] = useState([])
  const [currentConversationId, setCurrentConversationId] = useState(null)
  const [currentConversation, setCurrentConversation] = useState(null)
  const [apiKey, setApiKey] = useState('')
  const [loading, setLoading] = useState(false)

  // Load conversations on mount
  useEffect(() => {
    loadConversations()
  }, [])

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
    try {
      const convos = await api.listConversations()
      setConversations(convos)
    } catch (error) {
      console.error('Error loading conversations:', error)
    }
  }

  /**
   * Load current conversation details.
   */
  const loadCurrentConversation = async () => {
    try {
      const convo = await api.getConversation(currentConversationId)
      setCurrentConversation(convo)
    } catch (error) {
      console.error('Error loading conversation:', error)
    }
  }

  /**
   * Create a new conversation.
   */
  const handleNewConversation = async () => {
    try {
      const newConvo = await api.createConversation()
      setConversations([newConvo, ...conversations])
      setCurrentConversationId(newConvo.id)
    } catch (error) {
      console.error('Error creating conversation:', error)
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

    setLoading(true)

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
        apiKey || null
      )

      // Reload conversation list to update titles
      loadConversations()
    } catch (error) {
      console.error('Error sending message:', error)
      // TODO: Rollback optimistic update on error
    } finally {
      setLoading(false)
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

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto p-4">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Mirmer AI - Multi-LLM Consultation
        </h1>
        
        {/* API Key Input */}
        <div className="mb-4">
          <input
            type="password"
            placeholder="OpenRouter API Key (optional)"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg"
          />
        </div>

        {/* New Conversation Button */}
        <button
          onClick={handleNewConversation}
          className="mb-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          New Conversation
        </button>

        {/* Placeholder for chat interface */}
        {currentConversation && (
          <div className="bg-white rounded-lg shadow p-4">
            <h2 className="text-xl font-semibold mb-4">{currentConversation.title}</h2>
            <p className="text-gray-600">Messages: {currentConversation.messages?.length || 0}</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
