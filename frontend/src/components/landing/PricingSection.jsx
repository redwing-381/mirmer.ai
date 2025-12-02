import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '../ui/Card'
import { Button } from '../ui/Button'
import { Badge } from '../ui/Badge'
import AuthModal from '../AuthModal'
import UpgradeModal from '../UpgradeModal'
import EnterpriseContactModal from '../EnterpriseContactModal'
import { auth } from '../../firebase'
import { onAuthStateChanged } from 'firebase/auth'

export default function PricingSection() {
  const navigate = useNavigate()
  const [showAuthModal, setShowAuthModal] = useState(false)
  const [showUpgradeModal, setShowUpgradeModal] = useState(false)
  const [showEnterpriseModal, setShowEnterpriseModal] = useState(false)
  const [user, setUser] = useState(null)
  const [hoveredCard, setHoveredCard] = useState(null)

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser)
    })
    return () => unsubscribe()
  }, [])

  const handleGetStarted = (tier) => {
    if (tier === 'enterprise') {
      // Open enterprise contact modal
      setShowEnterpriseModal(true)
    } else if (tier === 'pro') {
      // For Pro tier
      if (user) {
        // User is logged in, show upgrade modal
        setShowUpgradeModal(true)
      } else {
        // User not logged in, show auth modal
        setShowAuthModal(true)
      }
    } else {
      // For Free tier
      if (user) {
        // User is logged in, redirect to app
        navigate('/app')
      } else {
        // User not logged in, show auth modal
        setShowAuthModal(true)
      }
    }
  }

  const pricingTiers = [
    {
      name: 'Free',
      price: '$0',
      period: '/month',
      description: 'Perfect for trying out Mirmer AI',
      features: [
        '10 queries per day',
        '3-stage council process',
        '4 AI models',
        'Conversation history',
        'Google Sign-In'
      ],
      cta: 'Get Started Free',
      highlighted: false
    },
    {
      name: 'Pro',
      price: '₹150',
      period: '/month',
      description: 'For power users who need more',
      features: [
        '100 queries per day',
        'Everything in Free',
        'Priority processing',
        'Extended history (90 days)',
        'Email support'
      ],
      cta: 'Start Pro Trial',
      highlighted: true
    },
    {
      name: 'Enterprise',
      price: 'Custom',
      period: '',
      description: 'For teams and organizations',
      features: [
        'Unlimited queries',
        'Everything in Pro',
        'Custom model selection',
        'API access',
        'Dedicated support',
        'SLA guarantee'
      ],
      cta: 'Contact Sales',
      highlighted: false
    }
  ]

  return (
    <section id="pricing" className="py-20 bg-[#f5f5f5] border-b-4 border-black">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-5xl md:text-6xl font-black text-black mb-6">
            SIMPLE PRICING
          </h2>
          <p className="text-xl text-gray-700 font-bold max-w-2xl mx-auto">
            Start free, upgrade when you need more
          </p>
        </div>

        {/* Pricing Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {pricingTiers.map((tier, index) => (
            <Card 
              key={index}
              className={`relative transition-all duration-300 cursor-pointer ${
                tier.highlighted 
                  ? 'bg-[#FFE66D] shadow-[12px_12px_0px_0px_rgba(0,0,0,1)]' 
                  : hoveredCard === index
                    ? 'shadow-[16px_16px_0px_0px_rgba(0,0,0,1)] -translate-y-2'
                    : 'shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]'
              }`}
              onMouseEnter={() => setHoveredCard(index)}
              onMouseLeave={() => setHoveredCard(null)}
            >
              {tier.highlighted && (
                <div className="absolute -top-5 left-1/2 transform -translate-x-1/2 z-10">
                  <div className="bg-[#FF6B6B] text-white border-4 border-black px-6 py-2 font-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] animate-pulse">
                    RECOMMENDED
                  </div>
                </div>
              )}
              
              <CardHeader>
                <CardTitle className="text-3xl">{tier.name.toUpperCase()}</CardTitle>
                <CardDescription className="font-bold text-base">{tier.description}</CardDescription>
                <div className="mt-6">
                  <span className={`text-5xl font-black transition-all duration-300 ${
                    hoveredCard === index ? 'text-6xl' : ''
                  }`}>{tier.price}</span>
                  <span className="text-gray-600 font-black text-xl">{tier.period}</span>
                </div>
              </CardHeader>

              <CardContent>
                <ul className="space-y-4">
                  {tier.features.map((feature, idx) => (
                    <li 
                      key={idx} 
                      className={`flex items-start transition-all duration-300 ${
                        hoveredCard === index ? 'translate-x-2' : ''
                      }`}
                      style={{ transitionDelay: `${idx * 50}ms` }}
                    >
                      <span className="text-[#4ECDC4] mr-3 font-black text-xl">✓</span>
                      <span className="font-bold text-gray-700">{feature}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>

              <CardFooter>
                <Button 
                  className={`w-full font-black text-lg transition-all duration-300 ${
                    tier.highlighted 
                      ? 'bg-[#FF6B6B] hover:bg-[#ff5252]' 
                      : 'bg-[#4ECDC4] hover:bg-[#3dbdb3]'
                  } ${hoveredCard === index ? 'scale-105' : ''}`}
                  onClick={() => handleGetStarted(tier.name.toLowerCase())}
                >
                  {tier.cta.toUpperCase()}
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>

        {/* Comparison tooltip */}
        <div className="mt-12 text-center">
          <div className="inline-block bg-white border-4 border-black px-8 py-4 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
            <p className="font-black text-lg">ALL PLANS INCLUDE THE 3-STAGE COUNCIL PROCESS</p>
          </div>
        </div>
      </div>

      <AuthModal isOpen={showAuthModal} onClose={() => setShowAuthModal(false)} />
      
      <UpgradeModal
        isOpen={showUpgradeModal}
        onClose={() => setShowUpgradeModal(false)}
      />

      <EnterpriseContactModal
        isOpen={showEnterpriseModal}
        onClose={() => setShowEnterpriseModal(false)}
      />
    </section>
  )
}
