import ReactMarkdown from 'react-markdown'

/**
 * Stage 3: Chairman Synthesis Component
 * Displays the final synthesized answer from the chairman.
 * 
 * Requirements: 7.4, 7.5
 */
export default function Stage3({ result, loading }) {
  if (loading) {
    return (
      <div className="p-6 bg-[#FF6B6B] border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
        <div className="flex items-center space-x-3">
          <div className="animate-spin rounded-full h-6 w-6 border-4 border-black border-t-transparent"></div>
          <span className="text-white font-black text-lg">STAGE 3: Chairman synthesizing final answer...</span>
        </div>
      </div>
    )
  }

  if (!result || !result.response) {
    return null
  }

  const modelName = result.model.split('/')[1] || result.model

  return (
    <div className="mb-6">
      <h3 className="text-2xl font-black mb-4">
        STAGE 3: Chairman's Final Synthesis
      </h3>
      
      <div className="bg-[#FF6B6B] border-4 border-black shadow-[12px_12px_0px_0px_rgba(0,0,0,1)] p-8">
        <div className="flex items-center mb-6">
          <span className="px-4 py-2 bg-black text-white text-sm font-black">
            CHAIRMAN: {modelName}
          </span>
        </div>
        
        <div className="prose max-w-none prose-headings:font-black prose-strong:font-black prose-p:text-lg text-white prose-headings:text-white prose-p:text-white prose-strong:text-white prose-li:text-white">
          <ReactMarkdown>{result.response}</ReactMarkdown>
        </div>
      </div>
    </div>
  )
}
