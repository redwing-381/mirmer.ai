import { useState } from 'react'
import ReactMarkdown from 'react-markdown'

/**
 * Stage 3: Chairman Synthesis Component
 * Displays the final synthesized answer from the chairman.
 * 
 * Requirements: 7.4, 7.5
 */
export default function Stage3({ result, loading }) {
  const [feedback, setFeedback] = useState(null) // 'up' or 'down'
  const [copied, setCopied] = useState(false)

  const handleThumbsUp = () => {
    setFeedback(feedback === 'up' ? null : 'up')
  }

  const handleThumbsDown = () => {
    setFeedback(feedback === 'down' ? null : 'down')
  }

  const handleCopy = async () => {
    if (result?.response) {
      try {
        await navigator.clipboard.writeText(result.response)
        setCopied(true)
        setTimeout(() => setCopied(false), 2000)
      } catch (err) {
        console.error('Failed to copy:', err)
      }
    }
  }
  if (loading) {
    return (
      <div className="p-6 bg-[#DDD6FE] border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
        <div className="flex items-center space-x-3">
          <div className="animate-spin rounded-full h-6 w-6 border-4 border-black border-t-transparent"></div>
          <span className="text-black font-black text-lg">STAGE 3: Chairman synthesizing final answer...</span>
        </div>
      </div>
    )
  }

  if (!result || !result.response) {
    return null
  }

  const modelName = result.model.split('/')[1] || result.model

  return (
    <div className="mb-4 md:mb-6">
      <h3 className="text-xl md:text-2xl font-black mb-3 md:mb-4">
        STAGE 3: Chairman's Final Synthesis
      </h3>
      
      <div className="bg-[#DDD6FE] border-4 border-black shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] md:shadow-[12px_12px_0px_0px_rgba(0,0,0,1)] p-4 md:p-8">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 sm:gap-0 mb-4 md:mb-6">
          <span className="px-3 md:px-4 py-2 bg-black text-white text-xs md:text-sm font-black">
            CHAIRMAN: {modelName}
          </span>
          
          {/* Action Buttons */}
          <div className="flex items-center gap-2">
            <button
              onClick={handleThumbsUp}
              className={`p-2 border-4 border-black transition-all min-h-[44px] min-w-[44px] flex items-center justify-center ${
                feedback === 'up'
                  ? 'bg-[#4ECDC4] shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]'
                  : 'bg-white shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[-2px] hover:translate-y-[-2px]'
              }`}
              title="Good response"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z" />
              </svg>
            </button>
            
            <button
              onClick={handleThumbsDown}
              className={`p-2 border-4 border-black transition-all min-h-[44px] min-w-[44px] flex items-center justify-center ${
                feedback === 'down'
                  ? 'bg-[#FFE66D] shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]'
                  : 'bg-white shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[-2px] hover:translate-y-[-2px]'
              }`}
              title="Bad response"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path d="M18 9.5a1.5 1.5 0 11-3 0v-6a1.5 1.5 0 013 0v6zM14 9.667v-5.43a2 2 0 00-1.105-1.79l-.05-.025A4 4 0 0011.055 2H5.64a2 2 0 00-1.962 1.608l-1.2 6A2 2 0 004.44 12H8v4a2 2 0 002 2 1 1 0 001-1v-.667a4 4 0 01.8-2.4l1.4-1.866a4 4 0 00.8-2.4z" />
              </svg>
            </button>
            
            <button
              onClick={handleCopy}
              className={`px-3 py-2 border-4 border-black font-black text-xs md:text-sm transition-all min-h-[44px] ${
                copied
                  ? 'bg-[#4ECDC4] shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]'
                  : 'bg-white shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[-2px] hover:translate-y-[-2px]'
              }`}
              title="Copy to clipboard"
            >
              {copied ? '✓ COPIED' : 'COPY'}
            </button>
          </div>
        </div>
        
        <div className="prose prose-sm md:prose-base lg:prose-lg max-w-none prose-headings:font-black prose-strong:font-black text-black prose-headings:text-black prose-p:text-black prose-strong:text-black prose-li:text-black overflow-x-auto">
          <ReactMarkdown>{result.response}</ReactMarkdown>
        </div>
      </div>
    </div>
  )
}
