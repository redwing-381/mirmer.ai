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
      <div className="p-6 bg-[#FFE66D] border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
        <div className="flex items-center space-x-3">
          <div className="animate-spin rounded-full h-6 w-6 border-4 border-black border-t-transparent"></div>
          <span className="text-black font-black text-lg">STAGE 2: Collecting peer rankings...</span>
        </div>
      </div>
    )
  }

  if (!rankings || rankings.length === 0) {
    return null
  }

  return (
    <div className="mb-4 md:mb-6">
      <h3 className="text-xl md:text-2xl font-black mb-3 md:mb-4">
        STAGE 2: Peer Rankings
      </h3>
      
      {/* Tab buttons - scrollable on mobile */}
      <div className="flex overflow-x-auto gap-2 mb-4 pb-2 -mx-2 px-2 md:mx-0 md:px-0 md:flex-wrap">
        {rankings.map((ranking, index) => {
          const modelName = ranking.model.split('/')[1] || ranking.model
          const isActive = activeTab === index
          
          return (
            <button
              key={index}
              onClick={() => setActiveTab(index)}
              className={`px-3 md:px-4 py-2 font-black border-4 border-black transition-all whitespace-nowrap text-sm md:text-base min-h-[44px] ${
                isActive
                  ? 'bg-[#FFE66D] text-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]'
                  : 'bg-white text-black shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[-2px] hover:translate-y-[-2px]'
              }`}
            >
              {modelName}
            </button>
          )
        })}
      </div>

      {/* Active tab content */}
      <div className="bg-white border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] md:shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] p-4 md:p-6 mb-4">
        <h4 className="font-black text-lg md:text-xl mb-3 md:mb-4">
          {rankings[activeTab].model.split('/')[1] || rankings[activeTab].model}'s Ranking
        </h4>
        
        <div className="prose prose-sm md:prose-base max-w-none mb-4 prose-headings:font-black prose-strong:font-black overflow-x-auto">
          <ReactMarkdown>{deAnonymizeText(rankings[activeTab].ranking)}</ReactMarkdown>
        </div>

        {/* Parsed ranking */}
        {rankings[activeTab].parsed_ranking && rankings[activeTab].parsed_ranking.length > 0 && (
          <div className="mt-4 p-3 md:p-4 bg-[#f5f5f5] border-4 border-black">
            <p className="font-black text-base md:text-lg mb-2 md:mb-3">Parsed Ranking:</p>
            <ol className="list-decimal list-inside space-y-2">
              {rankings[activeTab].parsed_ranking.map((label, idx) => {
                const model = metadata?.label_to_model?.[label]
                const modelName = model ? (model.split('/')[1] || model) : label
                return (
                  <li key={idx} className="font-bold text-sm md:text-base">
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
        <div className="bg-[#FFE66D] border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] md:shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] p-4 md:p-6">
          <h4 className="font-black text-xl md:text-2xl mb-4 md:mb-6">
            Aggregate Rankings
          </h4>
          
          <div className="space-y-2 md:space-y-3">
            {metadata.aggregate_rankings.map((item, index) => {
              const modelName = item.model.split('/')[1] || item.model
              const isWinner = index === 0
              
              return (
                <div
                  key={index}
                  className={`flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 sm:gap-0 p-3 md:p-4 border-4 border-black ${
                    isWinner 
                      ? 'bg-[#4ECDC4] shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] md:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)]' 
                      : 'bg-white shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] md:shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]'
                  }`}
                >
                  <div className="flex items-center space-x-3 md:space-x-4">
                    <span className={`font-black text-xl md:text-2xl ${isWinner ? 'text-black' : 'text-gray-600'}`}>
                      #{index + 1}
                    </span>
                    <span className="font-black text-base md:text-lg">{modelName}</span>
                  </div>
                  
                  <div className="flex items-center space-x-4 md:space-x-6 text-xs md:text-sm ml-8 sm:ml-0">
                    <span className="font-bold">
                      Avg: <span className="font-black text-base md:text-lg">{item.average_rank.toFixed(2)}</span>
                    </span>
                    <span className="font-bold">
                      Votes: <span className="font-black text-base md:text-lg">{item.rankings_count}</span>
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
