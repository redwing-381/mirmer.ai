import { Card, CardContent } from '../ui/Card'

export default function FeaturesSection() {
  const features = [
    {
      color: '#4ECDC4',
      title: 'MULTIPLE AI MODELS',
      description: 'GPT-4, Claude, Gemini, and more each provide their unique perspective on your question'
    },
    {
      color: '#FFE66D',
      title: 'PEER EVALUATION',
      description: 'Each AI evaluates and ranks the other responses for quality and accuracy'
    },
    {
      color: '#FF6B6B',
      title: 'SYNTHESIS',
      description: 'A lead model combines the best insights into one comprehensive answer'
    },
    {
      color: '#4ECDC4',
      title: 'COLLECTIVE INTELLIGENCE',
      description: 'Get more balanced, well-reasoned answers than any single AI can provide'
    }
  ]

  return (
    <section id="features" className="py-20 bg-white border-b-4 border-black">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
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
              className="hover:shadow-[12px_12px_0px_0px_rgba(0,0,0,1)] transition-all"
              style={{ backgroundColor: feature.color }}
            >
              <CardContent className="p-8">
                <h3 className="text-2xl font-black mb-4">{feature.title}</h3>
                <p className="font-bold text-gray-800 text-lg">{feature.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  )
}
