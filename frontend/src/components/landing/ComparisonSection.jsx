import { useState } from 'react'

export default function ComparisonSection() {
  const [hoveredSide, setHoveredSide] = useState(null)

  const singleAI = [
    'Single perspective',
    'Potential bias',
    'Limited context',
    'One model\'s limitations'
  ]

  const mirmerAI = [
    '4 AI perspectives',
    'Peer-reviewed answers',
    'Comprehensive analysis',
    'Best of all models'
  ]

  return (
    <section className="py-20 bg-[#f5f5f5] border-b-4 border-black">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-5xl md:text-6xl font-black text-black mb-6">
            WHY MIRMER AI?
          </h2>
          <p className="text-xl text-gray-700 font-bold max-w-2xl mx-auto">
            See the difference collective intelligence makes
          </p>
        </div>

        {/* Comparison Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl mx-auto">
          {/* Single AI */}
          <div
            className={`bg-white border-4 border-black p-8 transition-all duration-300 ${
              hoveredSide === 'single'
                ? 'shadow-[12px_12px_0px_0px_rgba(0,0,0,1)] -translate-y-2'
                : 'shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]'
            }`}
            onMouseEnter={() => setHoveredSide('single')}
            onMouseLeave={() => setHoveredSide(null)}
          >
            <div className="text-center mb-6">
              <div className="inline-block bg-gray-200 border-4 border-black px-6 py-3 mb-4">
                <h3 className="text-2xl font-black">SINGLE AI</h3>
              </div>
            </div>

            <ul className="space-y-4">
              {singleAI.map((item, index) => (
                <li key={index} className="flex items-start">
                  <span className="text-gray-400 mr-3 font-black text-xl">×</span>
                  <span className="font-bold text-gray-600">{item}</span>
                </li>
              ))}
            </ul>

            <div className="mt-8 p-4 bg-gray-100 border-4 border-black">
              <p className="font-black text-center">GOOD, BUT LIMITED</p>
            </div>
          </div>

          {/* Mirmer AI */}
          <div
            className={`bg-[#4ECDC4] border-4 border-black p-8 transition-all duration-300 ${
              hoveredSide === 'mirmer'
                ? 'shadow-[16px_16px_0px_0px_rgba(0,0,0,1)] -translate-y-4 scale-105'
                : 'shadow-[12px_12px_0px_0px_rgba(0,0,0,1)]'
            }`}
            onMouseEnter={() => setHoveredSide('mirmer')}
            onMouseLeave={() => setHoveredSide(null)}
          >
            <div className="text-center mb-6">
              <div className="inline-block bg-[#FF6B6B] text-white border-4 border-black px-6 py-3 mb-4 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
                <h3 className="text-2xl font-black">MIRMER AI</h3>
              </div>
            </div>

            <ul className="space-y-4">
              {mirmerAI.map((item, index) => (
                <li key={index} className="flex items-start">
                  <span className="text-[#FFE66D] mr-3 font-black text-xl">✓</span>
                  <span className="font-bold text-gray-800">{item}</span>
                </li>
              ))}
            </ul>

            <div className="mt-8 p-4 bg-[#FFE66D] border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
              <p className="font-black text-center">BETTER ANSWERS, GUARANTEED</p>
            </div>
          </div>
        </div>

        {/* Stats */}
        <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto">
          {[
            { value: '4X', label: 'More Perspectives' },
            { value: '3', label: 'Stage Process' },
            { value: '100%', label: 'Peer Reviewed' },
            { value: '1', label: 'Best Answer' }
          ].map((stat, index) => (
            <div
              key={index}
              className="bg-white border-4 border-black p-6 text-center hover:bg-[#FFE66D] transition-all duration-300 cursor-pointer hover:shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]"
            >
              <div className="font-black text-4xl mb-2">{stat.value}</div>
              <div className="font-bold text-sm">{stat.label}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
