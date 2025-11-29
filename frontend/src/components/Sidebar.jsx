/**
 * Sidebar Component
 * Displays list of conversations with titles and timestamps.
 * 
 * Requirements: 8.4, 8.5
 */
export default function Sidebar({ 
  conversations, 
  currentConversationId, 
  onSelectConversation, 
  onNewConversation 
}) {
  const formatDate = (isoString) => {
    if (!isoString) return ''
    const date = new Date(isoString)
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <div className="w-64 bg-white border-r border-gray-200 h-screen flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-900 mb-3">Conversations</h2>
        <button
          onClick={onNewConversation}
          className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
        >
          + New Conversation
        </button>
      </div>

      {/* Conversation List */}
      <div className="flex-1 overflow-y-auto">
        {conversations.length === 0 ? (
          <div className="p-4 text-center text-gray-500 text-sm">
            No conversations yet
          </div>
        ) : (
          <div className="py-2">
            {conversations.map((conversation) => {
              const isActive = conversation.id === currentConversationId
              
              return (
                <button
                  key={conversation.id}
                  onClick={() => onSelectConversation(conversation.id)}
                  className={`w-full text-left px-4 py-3 border-b border-gray-100 hover:bg-gray-50 transition-colors ${
                    isActive ? 'bg-blue-50 border-l-4 border-l-blue-600' : ''
                  }`}
                >
                  <div className="font-medium text-gray-900 text-sm truncate mb-1">
                    {conversation.title}
                  </div>
                  <div className="text-xs text-gray-500">
                    {formatDate(conversation.created_at)}
                  </div>
                </button>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}
