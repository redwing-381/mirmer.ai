import { useState } from 'react'
import { X, Check, Loader2 } from 'lucide-react'
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from './ui/Card'
import { Button } from './ui/Button'
import { Badge } from './ui/Badge'

export default function UpgradeModal({ isOpen, onClose, userEmail, userId }) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const loadRazorpayScript = () => {
    return new Promise((resolve) => {
      const script = document.createElement('script')
      script.src = 'https://checkout.razorpay.com/v1/checkout.js'
      script.onload = () => resolve(true)
      script.onerror = () => resolve(false)
      document.body.appendChild(script)
    })
  }

  const handleUpgrade = async () => {
    setLoading(true)
    setError(null)

    try {
      // Load Razorpay script
      const scriptLoaded = await loadRazorpayScript()
      if (!scriptLoaded) {
        throw new Error('Failed to load Razorpay SDK')
      }

      // Create subscription
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/payments/create-subscription`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-User-Id': userId,
          'X-User-Email': userEmail
        }
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to create subscription')
      }

      // Open Razorpay checkout
      const options = {
        key: import.meta.env.VITE_RAZORPAY_KEY_ID,
        subscription_id: data.subscription_id,
        name: 'Mirmer AI',
        description: 'Pro Plan Subscription',
        image: '/logo.png', // Add your logo
        prefill: {
          email: userEmail,
        },
        theme: {
          color: '#3B82F6'
        },
        handler: function (response) {
          // Payment successful
          window.location.href = `${window.location.origin}/app?payment=success`
        },
        modal: {
          ondismiss: function() {
            setLoading(false)
          }
        }
      }

      const razorpay = new window.Razorpay(options)
      razorpay.open()
    } catch (err) {
      console.error('Upgrade error:', err)
      setError(err.message)
      setLoading(false)
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-white border-b-4 border-black p-6 flex justify-between items-center">
          <h2 className="text-2xl font-black">Upgrade to Pro</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            disabled={loading}
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="p-6">
          {error && (
            <div className="mb-6 p-4 bg-red-50 border-4 border-red-500 rounded-lg">
              <p className="text-red-700 font-bold">{error}</p>
            </div>
          )}

          <Card className="ring-4 ring-yellow-400">
            <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
              <Badge variant="warning" className="text-sm px-4 py-1">
                RECOMMENDED
              </Badge>
            </div>

            <CardHeader>
              <CardTitle>Pro Plan</CardTitle>
              <CardDescription>For power users who need more</CardDescription>
              <div className="mt-4">
                <span className="text-5xl font-black">₹1,499</span>
                <span className="text-gray-600 font-bold">/month</span>
              </div>
            </CardHeader>

            <CardContent>
              <div className="space-y-4">
                <div>
                  <h3 className="font-bold text-lg mb-3">What's included:</h3>
                  <ul className="space-y-3">
                    {[
                      '100 queries per day',
                      '3-stage council process',
                      '4 AI models (GPT-4, Claude, Gemini, Llama)',
                      'Priority processing',
                      'Extended history (90 days)',
                      'Email support',
                      'Cancel anytime'
                    ].map((feature, idx) => (
                      <li key={idx} className="flex items-start">
                        <Check className="w-5 h-5 text-green-500 mr-3 flex-shrink-0 mt-0.5" />
                        <span className="text-gray-700">{feature}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="bg-blue-50 border-4 border-blue-200 rounded-lg p-4">
                  <p className="text-sm text-gray-700">
                    <strong>Secure payment powered by Razorpay.</strong> Your payment information is encrypted and never stored on our servers. Supports UPI, Cards, NetBanking, and Wallets.
                  </p>
                </div>
              </div>
            </CardContent>

            <CardFooter>
              <Button
                className="w-full"
                variant="primary"
                onClick={handleUpgrade}
                disabled={loading}
              >
                {loading ? (
                  <>
                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                    Processing...
                  </>
                ) : (
                  'Upgrade to Pro - ₹1,499/month'
                )}
              </Button>
            </CardFooter>
          </Card>

          <div className="mt-6 text-center text-sm text-gray-600">
            <p>Questions? Contact us at support@mirmer.ai</p>
          </div>
        </div>
      </div>
    </div>
  )
}
