import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '../ui/Card'
import { Button } from '../ui/Button'
import { Badge } from '../ui/Badge'
import { signInWithGoogle } from '../../firebase'
import UpgradeModal from '../UpgradeModal'

export default function PricingSection() {
  const navigate = useNavigate()
  const [showUpgradeModal, setShowUpgradeModal] = useState(false)
  const [userEmail, setUserEmail] = useState(null)
  const [userId, setUserId] = useState(null)

  const handleGetStarted = async (tier) => {
    try {
      const userCredential = await signInWithGoogle()
      const user = userCredential.user
      
      if (tier === 'pro') {
        // Show upgrade modal for Pro tier
        setUserEmail(user.email)
        setUserId(user.uid)
        setShowUpgradeModal(true)
      } else if (tier === 'enterprise') {
        // Redirect to contact page or open email
        window.location.href = 'mailto:sales@mirmer.ai?subject=Enterprise Plan Inquiry'
      } else {
        // Free tier - go directly to app
        navigate('/app')
      }
    } catch (error) {
      console.error('Sign in error:', error)
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
      price: '$19',
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
    <section id="pricing" className="py-20 bg-gradient-to-br from-blue-100 to-purple-100 border-b-4 border-black">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-black text-black mb-4">
            Simple Pricing
          </h2>
          <p className="text-lg text-gray-700 font-bold max-w-2xl mx-auto">
            Start free, upgrade when you need more
          </p>
        </div>

        {/* Pricing Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {pricingTiers.map((tier, index) => (
            <Card 
              key={index}
              className={`relative ${
                tier.highlighted 
                  ? 'ring-4 ring-yellow-400 scale-105' 
                  : ''
              }`}
            >
              {tier.highlighted && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                  <Badge variant="warning" className="text-sm px-4 py-1">
                    RECOMMENDED
                  </Badge>
                </div>
              )}
              
              <CardHeader>
                <CardTitle>{tier.name}</CardTitle>
                <CardDescription>{tier.description}</CardDescription>
                <div className="mt-4">
                  <span className="text-4xl font-black">{tier.price}</span>
                  <span className="text-gray-600 font-bold">{tier.period}</span>
                </div>
              </CardHeader>

              <CardContent>
                <ul className="space-y-3">
                  {tier.features.map((feature, idx) => (
                    <li key={idx} className="flex items-start">
                      <span className="text-green-500 mr-2 font-bold">✓</span>
                      <span className="text-gray-700">{feature}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>

              <CardFooter>
                <Button 
                  className="w-full"
                  variant={tier.highlighted ? 'primary' : 'default'}
                  onClick={() => handleGetStarted(tier.name.toLowerCase())}
                >
                  {tier.cta}
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      </div>

      <UpgradeModal
        isOpen={showUpgradeModal}
        onClose={() => setShowUpgradeModal(false)}
        userEmail={userEmail}
        userId={userId}
      />
    </section>
  )
}
