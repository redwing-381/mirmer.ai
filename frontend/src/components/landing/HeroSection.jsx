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
    <section className="relative bg-[#f5f5f5] border-b-4 border-black">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 md:py-32">
        <div className="text-center">
          {/* Headline */}
          <h1 className="text-5xl md:text-7xl font-black text-black mb-6 leading-tight">
            GET BETTER ANSWERS
            <br />
            FROM MULTIPLE AI MINDS
          </h1>

          {/* Subheadline */}
          <p className="text-xl md:text-2xl text-gray-700 font-bold mb-12 max-w-3xl mx-auto">
            Mirmer AI consults 4 leading AI models, ranks their responses, 
            and synthesizes the best answer for you
          </p>

          {/* CTA Button */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-20">
            <Button size="lg" className="bg-[#FF6B6B] hover:bg-[#ff5252] text-white" onClick={handleGetStarted}>
              START FREE - 10 QUERIES/DAY
            </Button>
          </div>

          {/* Visual Illustration */}
          <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
            <div className="bg-[#4ECDC4] border-4 border-black p-8 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] hover:shadow-[12px_12px_0px_0px_rgba(0,0,0,1)] transition-all">
              <div className="font-black text-2xl mb-4">STAGE 1</div>
              <div className="font-bold text-lg">4 AI Models Respond</div>
              <div className="text-sm font-bold mt-2 text-gray-700">Independent analysis from multiple perspectives</div>
            </div>
            
            <div className="bg-[#FFE66D] border-4 border-black p-8 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] hover:shadow-[12px_12px_0px_0px_rgba(0,0,0,1)] transition-all">
              <div className="font-black text-2xl mb-4">STAGE 2</div>
              <div className="font-bold text-lg">Models Rank Each Other</div>
              <div className="text-sm font-bold mt-2 text-gray-700">Peer evaluation determines quality</div>
            </div>
            
            <div className="bg-[#FF6B6B] border-4 border-black p-8 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] hover:shadow-[12px_12px_0px_0px_rgba(0,0,0,1)] transition-all text-white">
              <div className="font-black text-2xl mb-4">STAGE 3</div>
              <div className="font-bold text-lg">Chairman Synthesizes</div>
              <div className="text-sm font-bold mt-2">Final answer combines the best insights</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
