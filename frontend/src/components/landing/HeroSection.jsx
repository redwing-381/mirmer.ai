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
      color: '#DDD6FE',
      title: 'STAGE 3',
      subtitle: 'Chairman Synthesizes',
      description: 'Final answer combines the best insights',
      details: 'A lead model creates the optimal response'
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
          <p className="text-xl md:text-2xl text-gray-700 font-bold mb-6 max-w-3xl mx-auto animate-fade-in-delayed">
            Mirmer AI consults 4 leading AI models, ranks their responses, 
            and synthesizes the best answer for you
          </p>
          
          {/* Usage Options */}
          <div className="flex flex-wrap justify-center gap-4 mb-12 animate-fade-in-delayed">
            <div className="group px-6 py-3 bg-white border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[-2px] hover:translate-y-[-2px] transition-all cursor-default">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 bg-blue-400 border-2 border-black flex items-center justify-center group-hover:rotate-12 transition-transform">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 2a8 8 0 100 16 8 8 0 000-16zM9 9a1 1 0 112 0v4a1 1 0 11-2 0V9zm1-4a1 1 0 100 2 1 1 0 000-2z"/>
                  </svg>
                </div>
                <span className="font-bold text-sm">Web Application</span>
              </div>
            </div>
            <div className="group px-6 py-3 bg-white border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[-2px] hover:translate-y-[-2px] transition-all cursor-default">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 bg-green-400 border-2 border-black flex items-center justify-center group-hover:rotate-12 transition-transform">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                  </svg>
                </div>
                <span className="font-bold text-sm">Terminal / CLI</span>
              </div>
            </div>
            <div className="group px-6 py-3 bg-white border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[-2px] hover:translate-y-[-2px] transition-all cursor-default">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 bg-yellow-400 border-2 border-black flex items-center justify-center group-hover:rotate-12 transition-transform">
                  <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none">
                    <path d="M14.25.18l.9.2.73.26.59.3.45.32.34.34.25.34.16.33.1.3.04.26.02.2-.01.13V8.5l-.05.63-.13.55-.21.46-.26.38-.3.31-.33.25-.35.19-.35.14-.33.1-.3.07-.26.04-.21.02H8.77l-.69.05-.59.14-.5.22-.41.27-.33.32-.27.35-.2.36-.15.37-.1.35-.07.32-.04.27-.02.21v3.06H3.17l-.21-.03-.28-.07-.32-.12-.35-.18-.36-.26-.36-.36-.35-.46-.32-.59-.28-.73-.21-.88-.14-1.05-.05-1.23.06-1.22.16-1.04.24-.87.32-.71.36-.57.4-.44.42-.33.42-.24.4-.16.36-.1.32-.05.24-.01h.16l.06.01h8.16v-.83H6.18l-.01-2.75-.02-.37.05-.34.11-.31.17-.28.25-.26.31-.23.38-.2.44-.18.51-.15.58-.12.64-.1.71-.06.77-.04.84-.02 1.27.05zm-6.3 1.98l-.23.33-.08.41.08.41.23.34.33.22.41.09.41-.09.33-.22.23-.34.08-.41-.08-.41-.23-.33-.33-.22-.41-.09-.41.09zm13.09 3.95l.28.06.32.12.35.18.36.27.36.35.35.47.32.59.28.73.21.88.14 1.04.05 1.23-.06 1.23-.16 1.04-.24.86-.32.71-.36.57-.4.45-.42.33-.42.24-.4.16-.36.09-.32.05-.24.02-.16-.01h-8.22v.82h5.84l.01 2.76.02.36-.05.34-.11.31-.17.29-.25.25-.31.24-.38.2-.44.17-.51.15-.58.13-.64.09-.71.07-.77.04-.84.01-1.27-.04-1.07-.14-.9-.2-.73-.25-.59-.3-.45-.33-.34-.34-.25-.34-.16-.33-.1-.3-.04-.25-.02-.2.01-.13v-5.34l.05-.64.13-.54.21-.46.26-.38.3-.32.33-.24.35-.2.35-.14.33-.1.3-.06.26-.04.21-.02.13-.01h5.84l.69-.05.59-.14.5-.21.41-.28.33-.32.27-.35.2-.36.15-.36.1-.35.07-.32.04-.28.02-.21V6.07h2.09l.14.01zm-6.47 14.25l-.23.33-.08.41.08.41.23.33.33.23.41.08.41-.08.33-.23.23-.33.08-.41-.08-.41-.23-.33-.33-.23-.41-.08-.41.08z" fill="#3776AB"/>
                  </svg>
                </div>
                <span className="font-bold text-sm">Python SDK</span>
              </div>
            </div>
          </div>

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
