import { useState, useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { api } from '../api'
import Sidebar from '../components/Sidebar'
import ChatInterface from '../components/ChatInterface'
import { auth, logout } from '../firebase'
import { onAuthStateChanged } from 'firebase/auth'

function AppPage() {
  const navigate = useNavigate()
  const [searchParams, setSearchParams] = useSearchParams()
  
  // State management
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [conversations, setConversations] = useState([])
  const [currentConversationId, setCurrentConversationId] = useState(null)
  const [currentConversation, setCurrentConversation] = useState(null)
  const [messageLoading, setMessageLoading] = useState(false)
  const [paymentSuccess, setPaymentSuccess] = useState(false)

  // Listen for auth state changes
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser)
      setLoading(false)
      
      // Redirect to home if not authenticated
      if (!currentUser) {
        navigate('/')
      }
    })
    return () => unsubscribe()
  }, [navigate])

  // Check for payment success
  useEffect(() => {
    const payment = searchParams.get('payment')
    if (payment === 'success') {
      setPaymentSuccess(true)
      // Clear the query parameter
      setSearchParams({})
      // Hide notification after 5 seconds
      setTimeout(() => setPaymentSuccess(false), 5000)
    }
  }, [searchParams, setSearchParams])

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

  const loadConversations = async () => {
    if (!user) return
    try {
      const convos = await api.listConversations(user.uid)
      setConversations(convos)
    } catch (error) {
      console.error('Error loading conversations:', error)
    }
  }

  const loadCurrentConversation = async () => {
    if (!user) return
    try {
      const convo = await api.getConversation(currentConversationId, user.uid)
      setCurrentConversation(convo)
    } catch (error) {
      console.error('Error loading conversation:', error)
    }
  }

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

  const handleDeleteConversation = async (conversationId) => {
    if (!user) return
    try {
      await api.deleteConversation(conversationId, user.uid)
      setConversations(conversations.filter(c => c.id !== conversationId))
      
      if (conversationId === currentConversationId) {
        setCurrentConversationId(null)
        setCurrentConversation(null)
      }
    } catch (error) {
      console.error('Error deleting conversation:', error)
      alert('Failed to delete conversation')
    }
  }

  const handleSendMessage = async (content) => {
    if (!currentConversationId || !content.trim()) {
      return
    }

    setMessageLoading(true)

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
      await api.sendMessageStream(
        currentConversationId,
        content,
        (eventType, eventData) => {
          handleStreamEvent(eventType, eventData)
        },
        user.uid
      )

      loadConversations()
    } catch (error) {
      console.error('Error sending message:', error)
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
      navigate('/')
    } catch (error) {
      console.error('Error logging out:', error)
    }
  }

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

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="flex h-screen bg-[#f5f5f5]">
      {/* Payment Success Notification */}
      {paymentSuccess && (
        <div className="fixed top-4 right-4 z-50 bg-[#4ECDC4] text-black px-6 py-4 border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] animate-slide-in">
          <div className="flex items-center">
            <div>
              <p className="font-black text-lg">Payment Successful!</p>
              <p className="text-sm font-bold">Welcome to Pro! You now have 100 queries per day.</p>
            </div>
          </div>
        </div>
      )}

      <Sidebar
        conversations={conversations}
        currentConversationId={currentConversationId}
        onSelectConversation={setCurrentConversationId}
        onNewConversation={handleNewConversation}
        onDeleteConversation={handleDeleteConversation}
        userId={user.uid}
        user={user}
      />

      <div className="flex-1 flex flex-col">
        <div className="bg-white border-b-4 border-black p-6">
          <div className="flex items-center justify-between">
            <h1 className="text-4xl font-black">
              MIRMER AI
            </h1>
            
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-3 bg-[#4ECDC4] border-4 border-black px-4 py-2 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
                <img 
                  src={user.photoURL} 
                  alt={user.displayName}
                  className="w-8 h-8 border-2 border-black"
                />
                <span className="text-sm font-black">{user.displayName}</span>
              </div>
              <button
                onClick={handleLogout}
                className="px-4 py-2 text-sm bg-white border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] active:shadow-none active:translate-x-1 active:translate-y-1 transition-all font-black"
              >
                Logout
              </button>
            </div>
          </div>
        </div>

        <ChatInterface
          conversation={currentConversation}
          onSendMessage={handleSendMessage}
          loading={messageLoading}
        />
      </div>
    </div>
  )
}

export default AppPage
