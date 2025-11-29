import { useState } from 'react'
import ReactMarkdown from 'react-markdown'

/**
 * Stage 2: Peer Rankings Component
 * Displays peer rankings with de-anonymization and aggregate leaderboard.
 * 
 * Requirements: 7.2, 7.3, 7.5
 */
export default function Stage2({ rankings, metadata, loading }) {
  const [activeTab, setActiveTab] = useState(0)

  /**
   * De-anonymize text by replacing "Response X" labels with actual model names.
   */
  const deAnonymizeText = (text) => {
    if (!metadata?.label_to_model) return text

    let result = text
    for (const [label, model] of Object.entries(metadata.label_to_model)) {
      const modelName = model.split('/')[1] || model
      const regex = new RegExp(label, 'g')
      result = result.replace(regex, `${label} (${modelName})`)
    }
    return result
  }

  if (loading) {
    return (
      <div className="p-6 bg-purple-50 rounded-lg">
        <div className="flex items-center space-x-3">
          <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-purple-600"></div>
          <span className="text-purple-900 font-medium">Stage 2: Collecting peer rankings...</span>
        </div>
      </div>
    )
  }

  if (!rankings || rankings.length === 0) {
    return null
  }

  return (
    <div className="mb-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-3">
        Stage 2: Peer Rankings
      </h3>
      
      {/* Tab buttons */}
      <div className="flex space-x-2 mb-4 border-b border-gray-200">
        {rankings.map((ranking, index) => {
          const modelName = ranking.model.split('/')[1] || ranking.model
          const isActive = activeTab === index
          
          return (
            <button
              key={index}
              onClick={() => setActiveTab(index)}
              className={`px-4 py-2 font-medium transition-colors ${
                isActive
                  ? 'text-purple-600 border-b-2 border-purple-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              {modelName}
            </button>
          )
        })}
      </div>

      {/* Active tab content */}
      <div className="bg-white rounded-lg border border-gray-200 p-6 mb-4">
        <h4 className="font-semibold text-gray-900 mb-2">
          {rankings[activeTab].model.split('/')[1] || rankings[activeTab].model}'s Ranking
        </h4>
        
        <div className="prose max-w-none mb-4">
          <ReactMarkdown>{deAnonymizeText(rankings[activeTab].ranking)}</ReactMarkdown>
        </div>

        {/* Parsed ranking */}
        {rankings[activeTab].parsed_ranking && rankings[activeTab].parsed_ranking.length > 0 && (
          <div className="mt-4 p-4 bg-gray-50 rounded">
            <p className="font-medium text-gray-700 mb-2">Parsed Ranking:</p>
            <ol className="list-decimal list-inside space-y-1">
              {rankings[activeTab].parsed_ranking.map((label, idx) => {
                const model = metadata?.label_to_model?.[label]
                const modelName = model ? (model.split('/')[1] || model) : label
                return (
                  <li key={idx} className="text-gray-600">
                    {label} ({modelName})
                  </li>
                )
              })}
            </ol>
          </div>
        )}
      </div>

      {/* Aggregate Rankings Leaderboard */}
      {metadata?.aggregate_rankings && metadata.aggregate_rankings.length > 0 && (
        <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg border border-purple-200 p-6">
          <h4 className="font-semibold text-gray-900 mb-4 flex items-center">
            <span className="text-xl mr-2">🏆</span>
            Aggregate Rankings (Street Cred)
          </h4>
          
          <div className="space-y-3">
            {metadata.aggregate_rankings.map((item, index) => {
              const modelName = item.model.split('/')[1] || item.model
              const isWinner = index === 0
              
              return (
                <div
                  key={index}
                  className={`flex items-center justify-between p-3 rounded-lg ${
                    isWinner ? 'bg-yellow-100 border-2 border-yellow-400' : 'bg-white'
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <span className={`font-bold text-lg ${isWinner ? 'text-yellow-600' : 'text-gray-500'}`}>
                      #{index + 1}
                    </span>
                    <span className="font-medium text-gray-900">{modelName}</span>
                  </div>
                  
                  <div className="flex items-center space-x-4 text-sm">
                    <span className="text-gray-600">
                      Avg Rank: <span className="font-semibold">{item.average_rank.toFixed(2)}</span>
                    </span>
                    <span className="text-gray-600">
                      Votes: <span className="font-semibold">{item.rankings_count}</span>
                    </span>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      )}
    </div>
  )
}
