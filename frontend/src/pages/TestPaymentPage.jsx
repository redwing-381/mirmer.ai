import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import UpgradeModal from '../components/UpgradeModal'
import { auth } from '../firebase'
import { Button } from '../components/ui/Button'

export default function TestPaymentPage() {
  const [showModal, setShowModal] = useState(false)
  const navigate = useNavigate()
  const user = auth.currentUser

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="bg-white p-8 rounded-lg shadow-lg">
          <h1 className="text-2xl font-bold mb-4">Please Sign In First</h1>
          <Button onClick={() => navigate('/')}>Go to Home</Button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
        <h1 className="text-3xl font-black mb-4">Test Razorpay Payment</h1>
        <p className="text-gray-600 mb-6">
          Click the button below to test the Razorpay checkout modal.
        </p>
        
        <div className="mb-6 p-4 bg-blue-50 rounded-lg">
          <p className="text-sm font-bold mb-2">Signed in as:</p>
          <p className="text-sm">{user.email}</p>
          <p className="text-xs text-gray-500 mt-1">User ID: {user.uid}</p>
        </div>

        <Button
          className="w-full mb-4"
          variant="primary"
          onClick={() => setShowModal(true)}
        >
          Open Razorpay Checkout
        </Button>

        <Button
          className="w-full"
          variant="default"
          onClick={() => navigate('/app')}
        >
          Back to App
        </Button>

        <div className="mt-6 p-4 bg-yellow-50 rounded-lg">
          <p className="text-sm font-bold mb-2">Test Card:</p>
          <p className="text-sm font-mono">4111 1111 1111 1111</p>
          <p className="text-xs text-gray-600 mt-1">CVV: 123 | Expiry: 12/25</p>
        </div>
      </div>

      <UpgradeModal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        userEmail={user.email}
        userId={user.uid}
      />
    </div>
  )
}
