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
      <div className="p-6 bg-[#4ECDC4] border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
        <div className="flex items-center space-x-3">
          <div className="animate-spin rounded-full h-6 w-6 border-4 border-black border-t-transparent"></div>
          <span className="text-black font-black text-lg">STAGE 1: Collecting individual responses...</span>
        </div>
      </div>
    )
  }

  if (!responses || responses.length === 0) {
    return null
  }

  return (
    <div className="mb-6">
      <h3 className="text-2xl font-black mb-4">
        STAGE 1: Individual Responses
      </h3>
      
      {/* Tab buttons */}
      <div className="flex flex-wrap gap-2 mb-4">
        {responses.map((response, index) => {
          const modelName = response.model.split('/')[1] || response.model
          const isActive = activeTab === index
          
          return (
            <button
              key={index}
              onClick={() => setActiveTab(index)}
              className={`px-4 py-2 font-black border-4 border-black transition-all ${
                isActive
                  ? 'bg-[#4ECDC4] text-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]'
                  : 'bg-white text-black shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[-2px] hover:translate-y-[-2px]'
              }`}
            >
              {modelName}
            </button>
          )
        })}
      </div>

      {/* Active tab content */}
      <div className="bg-white border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] p-6">
        <div className="prose max-w-none prose-headings:font-black prose-strong:font-black">
          <ReactMarkdown>{responses[activeTab].response}</ReactMarkdown>
        </div>
      </div>
    </div>
  )
}
