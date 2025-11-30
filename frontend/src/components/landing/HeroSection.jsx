import { useNavigate } from 'react-router-dom'
import { Button } from '../ui/Button'
import { signInWithGoogle } from '../../firebase'

export default function HeroSection() {
  const navigate = useNavigate()

  const handleGetStarted = async () => {
    try {
      await signInWithGoogle()
      navigate('/app')
    } catch (error) {
      console.error('Sign in error:', error)
    }
  }

  return (
    <section className="relative bg-gradient-to-br from-yellow-200 via-pink-200 to-blue-200 border-b-4 border-black">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 md:py-32">
        <div className="text-center">
          {/* Headline */}
          <h1 className="text-4xl md:text-6xl font-black text-black mb-6 leading-tight">
            Get Better Answers from
            <br />
            <span className="text-blue-600">Multiple AI Minds</span>
          </h1>

          {/* Subheadline */}
          <p className="text-lg md:text-xl text-black font-bold mb-8 max-w-3xl mx-auto">
            Mirmer AI consults 4 leading AI models, ranks their responses, 
            and synthesizes the best answer for you
          </p>

          {/* CTA Button */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Button size="lg" variant="primary" onClick={handleGetStarted}>
              Start Free - 10 Queries/Day
            </Button>
          </div>

          {/* Visual Illustration */}
          <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            <div className="bg-white border-4 border-black p-6 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
              <div className="text-4xl mb-3">🤖</div>
              <div className="font-bold text-lg mb-2">Stage 1</div>
              <div className="text-sm">4 AI models respond</div>
            </div>
            
            <div className="bg-white border-4 border-black p-6 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
              <div className="text-4xl mb-3">⚖️</div>
              <div className="font-bold text-lg mb-2">Stage 2</div>
              <div className="text-sm">Models rank each other</div>
            </div>
            
            <div className="bg-white border-4 border-black p-6 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
              <div className="text-4xl mb-3">🎯</div>
              <div className="font-bold text-lg mb-2">Stage 3</div>
              <div className="text-sm">Chairman synthesizes</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
