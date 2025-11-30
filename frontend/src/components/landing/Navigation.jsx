import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Button } from '../ui/Button'
import { signInWithGoogle } from '../../firebase'

export default function Navigation({ user }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const navigate = useNavigate()

  const handleSignIn = async () => {
    try {
      await signInWithGoogle()
      navigate('/app')
    } catch (error) {
      console.error('Sign in error:', error)
    }
  }

  const scrollToSection = (id) => {
    const element = document.getElementById(id)
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' })
      setMobileMenuOpen(false)
    }
  }

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-white border-b-4 border-black shadow-[0px_4px_0px_0px_rgba(0,0,0,1)]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          {/* Logo */}
          <div className="flex-shrink-0">
            <h1 className="text-3xl font-black">MIRMER AI</h1>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <button
              onClick={() => scrollToSection('features')}
              className="text-black font-black hover:text-[#4ECDC4] transition-colors text-lg"
            >
              FEATURES
            </button>
            <button
              onClick={() => scrollToSection('pricing')}
              className="text-black font-black hover:text-[#FFE66D] transition-colors text-lg"
            >
              PRICING
            </button>
          </div>

          {/* Desktop Auth Buttons */}
          <div className="hidden md:flex items-center space-x-4">
            {user ? (
              <Button className="bg-[#4ECDC4] hover:bg-[#3dbdb3]" onClick={() => navigate('/app')}>
                GO TO APP
              </Button>
            ) : (
              <>
                <Button variant="neutral" onClick={handleSignIn}>
                  SIGN IN
                </Button>
                <Button className="bg-[#FF6B6B] hover:bg-[#ff5252]" onClick={handleSignIn}>
                  GET STARTED
                </Button>
              </>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-3 border-4 border-black bg-white hover:bg-gray-100 shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] active:shadow-none active:translate-x-[2px] active:translate-y-[2px] transition-all"
            >
              <svg
                className="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={3}
              >
                {mobileMenuOpen ? (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M6 18L18 6M6 6l12 12"
                  />
                ) : (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                )}
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t-4 border-black bg-white">
          <div className="px-4 pt-2 pb-4 space-y-3">
            <button
              onClick={() => scrollToSection('features')}
              className="block w-full text-left px-4 py-3 text-black font-black hover:bg-[#4ECDC4] border-2 border-black transition-all"
            >
              FEATURES
            </button>
            <button
              onClick={() => scrollToSection('pricing')}
              className="block w-full text-left px-4 py-3 text-black font-black hover:bg-[#FFE66D] border-2 border-black transition-all"
            >
              PRICING
            </button>
            <div className="pt-4 space-y-2">
              {user ? (
                <Button className="w-full bg-[#4ECDC4]" onClick={() => navigate('/app')}>
                  GO TO APP
                </Button>
              ) : (
                <>
                  <Button variant="neutral" className="w-full" onClick={handleSignIn}>
                    SIGN IN
                  </Button>
                  <Button className="w-full bg-[#FF6B6B]" onClick={handleSignIn}>
                    GET STARTED
                  </Button>
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </nav>
  )
}
