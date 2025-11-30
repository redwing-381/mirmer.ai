import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Settings, ChevronLeft, ChevronRight } from 'lucide-react'
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from './ui/AlertDialog'

/**
 * Sidebar Component
 * Displays list of conversations with titles and timestamps.
 * 
 * Requirements: 8.4, 8.5, 2.1, 2.2, 4.1, 4.2, 4.3, 4.4
 */
export default function Sidebar({ 
  conversations, 
  currentConversationId, 
  onSelectConversation, 
  onNewConversation,
  onDeleteConversation,
  isCollapsed = false,
  onToggleCollapse
}) {
  const navigate = useNavigate()
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false)
  const [conversationToDelete, setConversationToDelete] = useState(null)
  
  const handleDeleteClick = (conversationId) => {
    setConversationToDelete(conversationId)
    setDeleteDialogOpen(true)
  }
  
  const handleConfirmDelete = () => {
    if (conversationToDelete) {
      onDeleteConversation(conversationToDelete)
      setConversationToDelete(null)
    }
  }
  
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
    <>
      {/* Sidebar Content */}
      <div className={`fixed left-0 top-0 w-80 bg-white border-r-4 border-black h-screen flex flex-col transition-transform duration-300 ease-in-out z-40 ${isCollapsed ? '-translate-x-full' : 'translate-x-0'}`}>
        {/* Header */}
      <div className="p-4 border-b-4 border-black bg-[#4ECDC4]">
        <h2 className="text-2xl font-black mb-3">CONVERSATIONS</h2>
        <button
          onClick={onNewConversation}
          className="w-full px-4 py-3 bg-[#FF6B6B] text-white border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] active:shadow-none active:translate-x-1 active:translate-y-1 transition-all font-black"
        >
          + New Conversation
        </button>
      </div>

      {/* Conversation List */}
      <div className="flex-1 overflow-y-auto bg-[#f5f5f5]">
        {conversations.length === 0 ? (
          <div className="p-6 text-center">
            <div className="bg-white border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] p-4">
              <p className="font-black text-lg">No conversations yet</p>
              <p className="text-sm mt-2 font-bold">Start a new one</p>
            </div>
          </div>
        ) : (
          <div className="p-2 space-y-2">
            {conversations.map((conversation) => {
              const isActive = conversation.id === currentConversationId
              
              return (
                <div
                  key={conversation.id}
                  className={`group relative transition-all ${
                    isActive 
                      ? 'bg-[#FFE66D] border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]' 
                      : 'bg-white border-2 border-black hover:border-4 hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]'
                  }`}
                >
                  <button
                    onClick={() => onSelectConversation(conversation.id)}
                    className="w-full text-left px-4 py-3 pr-12"
                  >
                    <div className="font-black text-sm truncate mb-1">
                      {conversation.title}
                    </div>
                    <div className="text-xs font-bold text-gray-600">
                      {formatDate(conversation.created_at)}
                    </div>
                  </button>
                  
                  {/* Delete button */}
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      handleDeleteClick(conversation.id)
                    }}
                    className="absolute right-2 top-1/2 -translate-y-1/2 p-2 bg-[#FF6B6B] border-2 border-black text-white hover:bg-[#ff5252] opacity-0 group-hover:opacity-100 transition-opacity font-black text-xs"
                    title="Delete conversation"
                  >
                    ×
                  </button>
                </div>
              )
            })}
          </div>
        )}
      </div>

      {/* User Profile Menu */}
      <div className="p-4 border-t-4 border-black bg-white">
        <div className="relative">
          <button
            onClick={() => navigate('/settings')}
            className="w-full px-4 py-3 bg-white border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] active:shadow-none active:translate-x-1 active:translate-y-1 transition-all font-black flex items-center justify-center"
          >
            <Settings className="w-4 h-4 mr-2" />
            Settings
          </button>
        </div>
      </div>
      
      {/* Delete Confirmation Dialog */}
      <AlertDialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Delete Conversation?</AlertDialogTitle>
            <AlertDialogDescription>
              This action cannot be undone. This will permanently delete this conversation and all its messages.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction onClick={handleConfirmDelete}>
              Delete
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
      </div>
      
      {/* Toggle Button - Always Visible */}
      <button
        onClick={onToggleCollapse}
        className={`fixed top-1/2 -translate-y-1/2 z-50 p-3 bg-[#4ECDC4] border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] active:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] transition-all font-black ${isCollapsed ? 'left-0' : 'left-80'}`}
        aria-label={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        title={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
      >
        {isCollapsed ? (
          <ChevronRight className="w-5 h-5" />
        ) : (
          <ChevronLeft className="w-5 h-5" />
        )}
      </button>
    </>
  )
}
