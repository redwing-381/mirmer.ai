import { Card, CardContent } from '../ui/Card'

export default function FeaturesSection() {
  const features = [
    {
      icon: '🤖',
      title: '4 AI Models Respond',
      description: 'GPT-4, Claude, Gemini, and more each provide their unique perspective on your question'
    },
    {
      icon: '⚖️',
      title: 'Models Rank Each Other',
      description: 'Each AI evaluates and ranks the other responses for quality and accuracy'
    },
    {
      icon: '🎯',
      title: 'Chairman Synthesizes',
      description: 'A lead model combines the best insights into one comprehensive answer'
    },
    {
      icon: '✨',
      title: 'Collective Intelligence',
      description: 'Get more balanced, well-reasoned answers than any single AI can provide'
    }
  ]

  return (
    <section id="features" className="py-20 bg-white border-b-4 border-black">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-black text-black mb-4">
            How It Works
          </h2>
          <p className="text-lg text-gray-700 font-bold max-w-2xl mx-auto">
            The 3-stage council process ensures you get the best possible answer
          </p>
        </div>

        {/* Feature Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {features.map((feature, index) => (
            <Card 
              key={index}
              className="hover:translate-x-1 hover:translate-y-1 hover:shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] transition-all"
            >
              <CardContent>
                <div className="text-5xl mb-4">{feature.icon}</div>
                <h3 className="text-2xl font-bold mb-3">{feature.title}</h3>
                <p className="text-gray-700">{feature.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  )
}
