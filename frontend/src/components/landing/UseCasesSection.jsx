import { useState } from 'react'
import { Card, CardContent } from '../ui/Card'

export default function UseCasesSection() {
  const [activeCase, setActiveCase] = useState(0)

  const useCases = [
    {
      title: 'RESEARCH & ANALYSIS',
      description: 'Get comprehensive answers backed by multiple AI perspectives',
      example: 'Analyzing complex topics, literature reviews, market research',
      color: '#4ECDC4',
      icon: '01'
    },
    {
      title: 'CODE REVIEW & DEBUGGING',
      description: 'Multiple models review your code for bugs and improvements',
      example: 'Code optimization, security audits, architecture decisions',
      color: '#FFE66D',
      icon: '02'
    },
    {
      title: 'CONTENT CREATION',
      description: 'Generate well-rounded content with diverse AI input',
      example: 'Blog posts, technical docs, marketing copy, scripts',
      color: '#FF6B6B',
      icon: '03'
    },
    {
      title: 'PROBLEM SOLVING',
      description: 'Tackle complex problems with collective AI intelligence',
      example: 'Business strategy, technical challenges, decision making',
      color: '#4ECDC4',
      icon: '04'
    }
  ]

  return (
    <section className="py-20 bg-white border-b-4 border-black">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-5xl md:text-6xl font-black text-black mb-6">
            USE CASES
          </h2>
          <p className="text-xl text-gray-700 font-bold max-w-2xl mx-auto">
            See how Mirmer AI helps across different scenarios
          </p>
        </div>

        {/* Use Cases Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {useCases.map((useCase, index) => (
            <Card
              key={index}
              className={`transition-all duration-300 cursor-pointer relative overflow-hidden ${
                activeCase === index
                  ? 'shadow-[16px_16px_0px_0px_rgba(0,0,0,1)] -translate-y-2'
                  : 'shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] hover:shadow-[12px_12px_0px_0px_rgba(0,0,0,1)]'
              }`}
              style={{ backgroundColor: useCase.color }}
              onMouseEnter={() => setActiveCase(index)}
              onMouseLeave={() => setActiveCase(null)}
            >
              <CardContent className="p-8 relative">
                {/* Large number in background */}
                <div className="absolute top-4 right-4 text-9xl font-black opacity-10 select-none">
                  {useCase.icon}
                </div>

                <div className="relative z-10">
                  <h3 className="text-2xl font-black mb-4">{useCase.title}</h3>
                  <p className="font-bold text-gray-800 text-lg mb-4">
                    {useCase.description}
                  </p>

                  {/* Example box */}
                  <div
                    className={`mt-4 p-4 bg-white border-4 border-black transition-all duration-300 ${
                      activeCase === index ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
                    }`}
                  >
                    <p className="font-black text-sm mb-2">EXAMPLES:</p>
                    <p className="font-bold text-sm">{useCase.example}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* CTA */}
        <div className="mt-16 text-center">
          <div className="inline-block bg-black text-white border-4 border-black px-8 py-4 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
            <p className="font-black text-lg">
              READY TO TRY? START WITH 10 FREE QUERIES PER DAY
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}
