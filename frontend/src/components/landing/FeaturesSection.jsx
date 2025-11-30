import { useState } from 'react'
import { Card, CardContent } from '../ui/Card'

export default function FeaturesSection() {
  const [hoveredIndex, setHoveredIndex] = useState(null)

  const features = [
    {
      color: '#4ECDC4',
      title: 'MULTIPLE AI MODELS',
      description: 'GPT-4, Claude, Gemini, and more each provide their unique perspective on your question',
      stat: '4 Models',
      icon: '01'
    },
    {
      color: '#FFE66D',
      title: 'PEER EVALUATION',
      description: 'Each AI evaluates and ranks the other responses for quality and accuracy',
      stat: 'Ranked',
      icon: '02'
    },
    {
      color: '#FF6B6B',
      title: 'SYNTHESIS',
      description: 'A lead model combines the best insights into one comprehensive answer',
      stat: '1 Answer',
      icon: '03'
    },
    {
      color: '#4ECDC4',
      title: 'COLLECTIVE INTELLIGENCE',
      description: 'Get more balanced, well-reasoned answers than any single AI can provide',
      stat: 'Better',
      icon: '04'
    }
  ]

  return (
    <section id="features" className="py-20 bg-white border-b-4 border-black relative overflow-hidden">
      {/* Decorative elements */}
      <div className="absolute top-10 right-10 w-40 h-40 border-4 border-black opacity-10 pointer-events-none"></div>
      <div className="absolute bottom-10 left-10 w-32 h-32 border-4 border-black opacity-10 pointer-events-none"></div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-5xl md:text-6xl font-black text-black mb-6">
            HOW IT WORKS
          </h2>
          <p className="text-xl text-gray-700 font-bold max-w-2xl mx-auto">
            The 3-stage council process ensures you get the best possible answer
          </p>
        </div>

        {/* Feature Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {features.map((feature, index) => (
            <Card 
              key={index}
              className={`transition-all duration-300 cursor-pointer group ${
                hoveredIndex === index 
                  ? 'shadow-[16px_16px_0px_0px_rgba(0,0,0,1)] -translate-y-2' 
                  : 'shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] hover:shadow-[12px_12px_0px_0px_rgba(0,0,0,1)]'
              }`}
              style={{ backgroundColor: feature.color }}
              onMouseEnter={() => setHoveredIndex(index)}
              onMouseLeave={() => setHoveredIndex(null)}
            >
              <CardContent className="p-8 relative">
                {/* Large number in background */}
                <div className="absolute top-4 right-4 text-8xl font-black opacity-10 select-none">
                  {feature.icon}
                </div>
                
                <div className="relative z-10">
                  {/* Stat badge */}
                  <div className={`inline-block px-4 py-2 bg-black text-white border-4 border-black font-black mb-4 transition-transform duration-300 ${
                    hoveredIndex === index ? 'scale-110' : ''
                  }`}>
                    {feature.stat}
                  </div>
                  
                  <h3 className="text-2xl font-black mb-4">{feature.title}</h3>
                  <p className="font-bold text-gray-800 text-lg">{feature.description}</p>
                  
                  {/* Animated underline */}
                  <div className={`mt-6 h-1 bg-black transition-all duration-300 ${
                    hoveredIndex === index ? 'w-full' : 'w-0'
                  }`}></div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Interactive stats bar */}
        <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-4">
          {['4 AI Models', '3 Stages', '1 Best Answer', '100% Better'].map((stat, idx) => (
            <div 
              key={idx}
              className="bg-white border-4 border-black p-6 text-center hover:bg-black hover:text-white transition-all duration-300 cursor-pointer group"
            >
              <div className="font-black text-3xl mb-2">{stat.split(' ')[0]}</div>
              <div className="font-bold text-sm">{stat.split(' ').slice(1).join(' ')}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
