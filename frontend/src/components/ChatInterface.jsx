import { useState, useRef, useEffect } from 'react'
import Stage1 from './Stage1'
import Stage2 from './Stage2'
import Stage3 from './Stage3'

/**
 * ChatInterface Component
 * Displays messages and handles user input.
 * 
 * Requirements: 2.1, 2.2, 2.4
 */
export default function ChatInterface({ conversation, onSendMessage, loading }) {
  const [input, setInput] = useState('')
  const messagesEndRef = useRef(null)

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [conversation?.messages])

  const handleSubmit = (e) => {
    e.preventDefault()
    
    if (!input.trim() || loading) {
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
      <div className="flex-1 flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <h2 className="text-2xl font-semibold text-gray-700 mb-2">
            Welcome to Mirmer AI
          </h2>
          <p className="text-gray-500">
            Create a new conversation to get started
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex-1 flex flex-col bg-gray-50">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6">
        <div className="max-w-4xl mx-auto space-y-6">
          {conversation.messages?.map((message, index) => (
            <div key={index}>
              {message.role === 'user' ? (
                // User Message
                <div className="flex justify-end mb-4">
                  <div className="bg-blue-600 text-white rounded-lg px-4 py-3 max-w-2xl">
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
                    <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                      <p className="text-red-800 font-medium">Error:</p>
                      <p className="text-red-600">{message.error}</p>
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
      <div className="border-t border-gray-200 bg-white p-4">
        <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
          <div className="flex space-x-4">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask your question... (10-2000 characters)"
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              rows="3"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !input.trim() || input.trim().length < 10}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors font-medium"
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
          <p className="text-xs text-gray-500 mt-2">
            Press Enter to send, Shift+Enter for new line
          </p>
        </form>
      </div>
    </div>
  )
}
