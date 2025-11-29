import { useState } from 'react'
import ReactMarkdown from 'react-markdown'

/**
 * Stage 1: Individual Responses Component
 * Displays responses from all council models in a tabbed interface.
 * 
 * Requirements: 7.1, 7.5
 */
export default function Stage1({ responses, loading }) {
  const [activeTab, setActiveTab] = useState(0)

  if (loading) {
    return (
      <div className="p-6 bg-blue-50 rounded-lg">
        <div className="flex items-center space-x-3">
          <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
          <span className="text-blue-900 font-medium">Stage 1: Collecting individual responses...</span>
        </div>
      </div>
    )
  }

  if (!responses || responses.length === 0) {
    return null
  }

  return (
    <div className="mb-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-3">
        Stage 1: Individual Responses
      </h3>
      
      {/* Tab buttons */}
      <div className="flex space-x-2 mb-4 border-b border-gray-200">
        {responses.map((response, index) => {
          const modelName = response.model.split('/')[1] || response.model
          const isActive = activeTab === index
          
          return (
            <button
              key={index}
              onClick={() => setActiveTab(index)}
              className={`px-4 py-2 font-medium transition-colors ${
                isActive
                  ? 'text-blue-600 border-b-2 border-blue-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              {modelName}
            </button>
          )
        })}
      </div>

      {/* Active tab content */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="prose max-w-none">
          <ReactMarkdown>{responses[activeTab].response}</ReactMarkdown>
        </div>
      </div>
    </div>
  )
}
