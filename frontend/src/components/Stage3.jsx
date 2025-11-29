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
      <div className="p-6 bg-green-50 rounded-lg">
        <div className="flex items-center space-x-3">
          <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-green-600"></div>
          <span className="text-green-900 font-medium">Stage 3: Chairman synthesizing final answer...</span>
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
      <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center">
        <span className="text-2xl mr-2">⚖️</span>
        Stage 3: Chairman's Final Synthesis
      </h3>
      
      <div className="bg-gradient-to-br from-green-50 to-blue-50 rounded-lg border-2 border-green-300 p-6 shadow-lg">
        <div className="flex items-center mb-4">
          <span className="px-3 py-1 bg-green-600 text-white text-sm font-medium rounded-full">
            Chairman: {modelName}
          </span>
        </div>
        
        <div className="prose max-w-none">
          <ReactMarkdown>{result.response}</ReactMarkdown>
        </div>
      </div>
    </div>
  )
}
