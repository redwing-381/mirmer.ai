import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { auth } from '../firebase'
import { onAuthStateChanged } from 'firebase/auth'
import Navigation from '../components/landing/Navigation'
import HeroSection from '../components/landing/HeroSection'
import FeaturesSection from '../components/landing/FeaturesSection'
import PricingSection from '../components/landing/PricingSection'
import Footer from '../components/landing/Footer'

function LandingPage() {
  const navigate = useNavigate()
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser)
      setLoading(false)
      
      // Redirect authenticated users to app
      if (currentUser) {
        navigate('/app')
      }
    })
    return () => unsubscribe()
  }, [navigate])

  if (loading) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-4 border-black"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-white">
      <Navigation user={user} />
      
      <main className="pt-16">
        <HeroSection />
        <FeaturesSection />
        <PricingSection />
      </main>
      
      <Footer />
    </div>
  )
}

export default LandingPage
