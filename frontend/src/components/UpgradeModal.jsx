import { useState, useEffect } from 'react'
import { X, Check, Loader2, Zap, Target, Bot, Rocket, MessageCircle, Lock } from 'lucide-react'
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from './ui/Card'
import { auth } from '../firebase'

export default function UpgradeModal({ isOpen, onClose }) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [user, setUser] = useState(null)

  useEffect(() => {
    const currentUser = auth.currentUser
    setUser(currentUser)
  }, [isOpen])

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
      console.log('Starting upgrade process...')
      console.log('User:', user)
      console.log('API URL:', import.meta.env.VITE_API_URL)
      console.log('Razorpay Key:', import.meta.env.VITE_RAZORPAY_KEY_ID)

      if (!user) {
        throw new Error('Please sign in to upgrade')
      }

      // Load Razorpay script
      console.log('Loading Razorpay script...')
      const scriptLoaded = await loadRazorpayScript()
      if (!scriptLoaded) {
        throw new Error('Failed to load Razorpay SDK')
      }
      console.log('Razorpay script loaded successfully')

      // Create subscription
      const apiUrl = import.meta.env.VITE_API_URL || ''
      const fullUrl = `${apiUrl}/api/payments/create-subscription`
      console.log('Creating subscription at:', fullUrl)

      const response = await fetch(fullUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-User-Id': user.uid,
          'X-User-Email': user.email
        }
      })

      console.log('Response status:', response.status)
      const data = await response.json()
      console.log('Response data:', data)

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to create subscription')
      }

      // Open Razorpay checkout
      const razorpayKey = import.meta.env.VITE_RAZORPAY_KEY_ID
      if (!razorpayKey) {
        throw new Error('Razorpay key not configured. Please contact support.')
      }

      console.log('Opening Razorpay checkout...')
      const options = {
        key: razorpayKey,
        subscription_id: data.subscription_id,
        name: 'Mirmer AI',
        description: 'Pro Plan Subscription',
        prefill: {
          email: user?.email,
        },
        theme: {
          color: '#4ECDC4'
        },
        handler: function (paymentResponse) {
          console.log('Payment successful:', paymentResponse)
          // Payment successful
          window.location.href = `${window.location.origin}/app?payment=success`
        },
        modal: {
          ondismiss: function() {
            console.log('Payment modal dismissed')
            setLoading(false)
          }
        }
      }

      const razorpay = new window.Razorpay(options)
      razorpay.open()
      console.log('Razorpay checkout opened')
    } catch (err) {
      console.error('Upgrade error:', err)
      setError(err.message || 'An error occurred. Please try again.')
      setLoading(false)
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4 overflow-y-auto backdrop-blur-sm">
      <div className="bg-white max-w-2xl w-full my-8 border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
        <div className="bg-teal-400 border-b-4 border-black p-6 flex justify-between items-center">
          <h2 className="text-2xl font-bold text-black">Upgrade to Pro</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-black/10 border-2 border-black transition-colors"
            disabled={loading}
          >
            <X className="w-5 h-5 text-black" />
          </button>
        </div>

        <div className="p-6">
          {error && (
            <div className="mb-4 p-4 bg-red-100 border-4 border-red-500 shadow-[4px_4px_0px_0px_rgba(239,68,68,1)]">
              <p className="text-red-700 font-bold">{error}</p>
            </div>
          )}

          <Card>
            <CardHeader className="pb-4 bg-yellow-100 border-b-4 border-black -m-6 mb-6 p-6">
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-2xl">Pro Plan</CardTitle>
                  <CardDescription className="text-sm font-semibold text-gray-700">Unlock your full potential</CardDescription>
                </div>
                <div className="text-right bg-white border-4 border-black px-5 py-3 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
                  <div className="text-3xl font-black text-teal-600">₹1,499</div>
                  <div className="text-xs text-gray-700 font-bold">/month</div>
                </div>
              </div>
            </CardHeader>

            <CardContent>
              <ul className="space-y-3">
                {[
                  { text: '100 queries per day', Icon: Zap },
                  { text: '3-stage council process', Icon: Target },
                  { text: '4 AI models working together', Icon: Bot },
                  { text: 'Priority processing', Icon: Rocket },
                  { text: 'Email support', Icon: MessageCircle }
                ].map((feature, idx) => (
                  <li key={idx} className="flex items-center gap-3">
                    <div className="flex-shrink-0 w-10 h-10 bg-teal-400 border-2 border-black flex items-center justify-center shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]">
                      <feature.Icon className="w-5 h-5 text-white" strokeWidth={2.5} />
                    </div>
                    <Check className="w-5 h-5 text-emerald-600 flex-shrink-0" strokeWidth={3} />
                    <span className="text-gray-800 font-semibold">{feature.text}</span>
                  </li>
                ))}
              </ul>

              <div className="bg-blue-100 border-4 border-blue-500 p-4 mt-6 flex items-start gap-3 shadow-[4px_4px_0px_0px_rgba(59,130,246,1)]">
                <Lock className="w-5 h-5 text-blue-700 flex-shrink-0 mt-0.5" strokeWidth={2.5} />
                <p className="text-sm text-gray-800 font-semibold">
                  <span className="font-bold">Secure payment by Razorpay.</span> Supports UPI, Cards, NetBanking & Wallets.
                </p>
              </div>
            </CardContent>

            <CardFooter>
              <button
                onClick={handleUpgrade}
                disabled={loading}
                className="w-full px-8 py-4 bg-teal-500 hover:bg-teal-600 text-white border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:translate-x-boxShadowX hover:translate-y-boxShadowY hover:shadow-none active:shadow-none disabled:bg-gray-400 disabled:cursor-not-allowed disabled:hover:translate-x-0 disabled:hover:translate-y-0 transition-all duration-150 font-bold text-lg"
              >
                {loading ? (
                  <span className="flex items-center justify-center">
                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                    Processing...
                  </span>
                ) : (
                  'Upgrade to Pro Now'
                )}
              </button>
            </CardFooter>
          </Card>
        </div>
      </div>
    </div>
  )
}
