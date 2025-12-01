import { useState, useRef, useEffect } from 'react'
import Stage1 from './Stage1'
import Stage2 from './Stage2'
import Stage3 from './Stage3'
import UpgradeModal from './UpgradeModal'
import ExportMenu from './ExportMenu'

/**
 * ChatInterface Component
 * Displays messages and handles user input.
 * 
 * Requirements: 2.1, 2.2, 2.4, 3.1
 */
export default function ChatInterface({ conversation, onSendMessage, loading, usageStats, userId }) {
  const [input, setInput] = useState('')
  const messagesEndRef = useRef(null)
  const [showUpgradeModal, setShowUpgradeModal] = useState(false)

  // Check if user has reached their limit
  const isOverLimit = usageStats && usageStats.daily_queries_used >= usageStats.daily_limit

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [conversation?.messages])

  const handleSubmit = (e) => {
    e.preventDefault()
    
    if (!input.trim() || loading) {
      return
    }

    // Check if over limit
    if (isOverLimit) {
      setShowUpgradeModal(true)
      return
    }

    // Validate length (10-2000 characters)
    if (input.trim().length < 10) {
      alert('Message must be at least 10 characters long')
      return
    }

    if (input.trim().length > 2000) {
      alert('Message must be less than 2000 characters')
      return
    }

    onSendMessage(input.trim())
    setInput('')
  }

  const handleKeyDown = (e) => {
    // Submit on Enter, new line on Shift+Enter
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  if (!conversation) {
    return (
      <div className="flex-1 flex items-center justify-center bg-[#f5f5f5]" style={{
        backgroundImage: `
          linear-gradient(rgba(0, 0, 0, 0.06) 1px, transparent 1px),
          linear-gradient(90deg, rgba(0, 0, 0, 0.06) 1px, transparent 1px)
        `,
        backgroundSize: '40px 40px'
      }}>
        <div className="text-center">
          <div className="bg-white border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] p-12 max-w-md">
            <h2 className="text-3xl font-black mb-4">
              Welcome to Mirmer AI
            </h2>
            <p className="text-lg font-bold text-gray-600">
              Create a new conversation to get started
            </p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="flex-1 flex flex-col bg-[#f5f5f5] min-h-0">
      {/* Header with Export Button */}
      <div className="border-b-4 border-black bg-white px-6 py-4 flex-shrink-0">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div className="flex-1 min-w-0">
            <h1 className="text-xl font-black truncate">{conversation.title || 'New Conversation'}</h1>
          </div>
          {conversation.messages && conversation.messages.length > 0 && (
            <div className="ml-4">
              <ExportMenu conversationId={conversation.id} userId={userId} />
            </div>
          )}
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6 min-h-0" style={{
        backgroundImage: `
          linear-gradient(rgba(0, 0, 0, 0.06) 1px, transparent 1px),
          linear-gradient(90deg, rgba(0, 0, 0, 0.06) 1px, transparent 1px)
        `,
        backgroundSize: '40px 40px'
      }}>
        <div className="max-w-4xl mx-auto space-y-6">
          {conversation.messages?.map((message, index) => (
            <div key={index}>
              {message.role === 'user' ? (
                // User Message
                <div className="flex justify-end mb-4">
                  <div className="bg-[#4ECDC4] border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] px-6 py-4 max-w-2xl font-bold">
                    <p className="whitespace-pre-wrap">{message.content}</p>
                  </div>
                </div>
              ) : (
                // Assistant Message with 3 Stages
                <div className="space-y-4">
                  <Stage1 
                    responses={message.stage1} 
                    loading={message.loading?.stage1}
                  />
                  
                  <Stage2 
                    rankings={message.stage2} 
                    metadata={message.metadata}
                    loading={message.loading?.stage2}
                  />
                  
                  <Stage3 
                    result={message.stage3} 
                    loading={message.loading?.stage3}
                  />

                  {message.error && (
                    <div className="p-6 bg-[#FCA5A5] border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
                      <p className="text-black font-black text-lg mb-2">ERROR</p>
                      <p className="text-black font-bold">{message.error}</p>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
          
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="border-t-4 border-black bg-white p-6 flex-shrink-0">
        <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
          {isOverLimit && (
            <div className="mb-4 p-4 bg-[#FFE66D] border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
              <p className="font-black text-lg mb-2">⚠️ Daily Limit Reached!</p>
              <p className="font-bold mb-3">You've used all {usageStats.daily_limit} queries for today.</p>
              <button
                type="button"
                onClick={() => setShowUpgradeModal(true)}
                className="px-6 py-2 bg-[#FF6B6B] text-white border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] font-black"
              >
                UPGRADE TO PRO
              </button>
            </div>
          )}
          
          <div className="flex space-x-4">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={isOverLimit ? "Daily limit reached. Upgrade to continue..." : "Ask your question... (10-2000 characters)"}
              className="flex-1 px-4 py-3 border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] focus:outline-none focus:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] resize-none font-medium transition-all disabled:bg-gray-100 disabled:cursor-not-allowed"
              rows="3"
              disabled={loading || isOverLimit}
            />
            <button
              type="submit"
              disabled={loading || !input.trim() || input.trim().length < 10 || isOverLimit}
              className="px-8 py-3 bg-[#FF6B6B] text-white border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] active:shadow-none active:translate-x-1 active:translate-y-1 disabled:bg-gray-300 disabled:cursor-not-allowed transition-all font-black text-lg"
            >
              {loading ? (
                <div className="flex items-center space-x-2">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  <span>Processing...</span>
                </div>
              ) : (
                'Send'
              )}
            </button>
          </div>
          <p className="text-sm font-bold mt-3 text-gray-600">
            {isOverLimit ? (
              <span className="text-[#FF6B6B]">Upgrade to Pro for 100 queries/day</span>
            ) : (
              'Press Enter to send • Shift+Enter for new line'
            )}
          </p>
        </form>
      </div>
      
      {/* Upgrade Modal */}
      {showUpgradeModal && (
        <UpgradeModal onClose={() => setShowUpgradeModal(false)} />
      )}
    </div>
  )
}
