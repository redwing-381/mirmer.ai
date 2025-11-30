import { useState } from 'react'
import { Button } from '../ui/Button'
import AuthModal from '../AuthModal'

export default function HeroSection() {
  const [activeStage, setActiveStage] = useState(null)
  const [showAuthModal, setShowAuthModal] = useState(false)

  const handleGetStarted = () => {
    setShowAuthModal(true)
  }

  const stages = [
    {
      id: 1,
      color: '#4ECDC4',
      title: 'STAGE 1',
      subtitle: '4 AI Models Respond',
      description: 'Independent analysis from multiple perspectives',
      details: 'GPT-4, Claude, Gemini, and more provide unique insights'
    },
    {
      id: 2,
      color: '#FFE66D',
      title: 'STAGE 2',
      subtitle: 'Models Rank Each Other',
      description: 'Peer evaluation determines quality',
      details: 'Each model evaluates others for accuracy and depth'
    },
    {
      id: 3,
      color: '#FF6B6B',
      title: 'STAGE 3',
      subtitle: 'Chairman Synthesizes',
      description: 'Final answer combines the best insights',
      details: 'A lead model creates the optimal response',
      textWhite: true
    }
  ]

  return (
    <section className="relative bg-[#f5f5f5] border-b-4 border-black overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-32 h-32 border-4 border-black bg-[#4ECDC4] opacity-20 animate-float"></div>
        <div className="absolute top-40 right-20 w-24 h-24 border-4 border-black bg-[#FFE66D] opacity-20 animate-float-delayed"></div>
        <div className="absolute bottom-20 left-1/4 w-20 h-20 border-4 border-black bg-[#FF6B6B] opacity-20 animate-float"></div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 md:py-32 relative z-10">
        <div className="text-center">
          {/* Headline with subtle animation */}
          <h1 className="text-5xl md:text-7xl font-black text-black mb-6 leading-tight animate-fade-in">
            GET BETTER ANSWERS
            <br />
            FROM MULTIPLE AI MINDS
          </h1>

          {/* Subheadline */}
          <p className="text-xl md:text-2xl text-gray-700 font-bold mb-12 max-w-3xl mx-auto animate-fade-in-delayed">
            Mirmer AI consults 4 leading AI models, ranks their responses, 
            and synthesizes the best answer for you
          </p>

          {/* CTA Button with pulse effect */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-20">
            <Button 
              size="lg" 
              className="bg-[#FF6B6B] hover:bg-[#ff5252] text-white relative group" 
              onClick={handleGetStarted}
            >
              <span className="relative z-10">START FREE - 10 QUERIES/DAY</span>
              <div className="absolute inset-0 bg-[#ff5252] opacity-0 group-hover:opacity-100 transition-opacity"></div>
            </Button>
          </div>

          {/* Interactive Stage Cards */}
          <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
            {stages.map((stage) => (
              <div
                key={stage.id}
                className={`border-4 border-black p-8 cursor-pointer transition-all duration-300 ${
                  activeStage === stage.id 
                    ? 'shadow-[16px_16px_0px_0px_rgba(0,0,0,1)] scale-105 -translate-y-2' 
                    : 'shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] hover:shadow-[12px_12px_0px_0px_rgba(0,0,0,1)] hover:-translate-y-1'
                } ${stage.textWhite ? 'text-white' : ''}`}
                style={{ backgroundColor: stage.color }}
                onMouseEnter={() => setActiveStage(stage.id)}
                onMouseLeave={() => setActiveStage(null)}
              >
                <div className="font-black text-2xl mb-4">{stage.title}</div>
                <div className="font-bold text-lg mb-2">{stage.subtitle}</div>
                <div className={`text-sm font-bold mt-2 ${stage.textWhite ? '' : 'text-gray-700'}`}>
                  {stage.description}
                </div>
                
                {/* Expandable details on hover */}
                <div className={`mt-4 pt-4 border-t-2 border-black transition-all duration-300 overflow-hidden ${
                  activeStage === stage.id ? 'max-h-20 opacity-100' : 'max-h-0 opacity-0'
                }`}>
                  <div className="text-sm font-bold">{stage.details}</div>
                </div>
              </div>
            ))}
          </div>

          {/* Interactive flow indicator */}
          <div className="mt-12 flex justify-center items-center gap-4">
            {[1, 2, 3].map((num) => (
              <div key={num} className="flex items-center">
                <div 
                  className={`w-12 h-12 border-4 border-black flex items-center justify-center font-black transition-all duration-300 ${
                    activeStage === num 
                      ? 'bg-black text-white scale-110' 
                      : 'bg-white text-black'
                  }`}
                >
                  {num}
                </div>
                {num < 3 && (
                  <div className="w-8 h-1 bg-black mx-2"></div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>

      <AuthModal isOpen={showAuthModal} onClose={() => setShowAuthModal(false)} />

      <style jsx>{`
        @keyframes float {
          0%, 100% { transform: translateY(0px) rotate(0deg); }
          50% { transform: translateY(-20px) rotate(5deg); }
        }
        
        @keyframes float-delayed {
          0%, 100% { transform: translateY(0px) rotate(0deg); }
          50% { transform: translateY(-15px) rotate(-5deg); }
        }

        @keyframes fade-in {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }

        .animate-float {
          animation: float 6s ease-in-out infinite;
        }

        .animate-float-delayed {
          animation: float-delayed 8s ease-in-out infinite;
        }

        .animate-fade-in {
          animation: fade-in 0.8s ease-out;
        }

        .animate-fade-in-delayed {
          animation: fade-in 0.8s ease-out 0.2s both;
        }
      `}</style>
    </section>
  )
}
