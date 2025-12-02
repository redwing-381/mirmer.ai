import { useState } from 'react'
import { X } from 'lucide-react'
import { Button } from './ui/Button'
import { Input } from './ui/Input'

export default function SubscriptionSupportModal({ isOpen, onClose, user }) {
  const [formData, setFormData] = useState({
    name: user?.displayName || '',
    email: user?.email || '',
    subject: '',
    message: ''
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitStatus, setSubmitStatus] = useState(null) // 'success' | 'error' | null

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsSubmitting(true)
    setSubmitStatus(null)

    try {
      const apiUrl = import.meta.env.VITE_API_URL || ''
      const response = await fetch(`${apiUrl}/api/subscription/support`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-User-Id': user?.uid
        },
        body: JSON.stringify(formData)
      })

      if (response.ok) {
        setSubmitStatus('success')
        // Reset message field
        setFormData({
          ...formData,
          subject: '',
          message: ''
        })
        // Close modal after 3 seconds
        setTimeout(() => {
          onClose()
          setSubmitStatus(null)
        }, 3000)
      } else {
        setSubmitStatus('error')
      }
    } catch (error) {
      console.error('Error submitting support request:', error)
      setSubmitStatus('error')
    } finally {
      setIsSubmitting(false)
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
      <div className="relative w-full max-w-lg bg-white border-4 border-black shadow-[12px_12px_0px_0px_rgba(0,0,0,1)]">
        {/* Header */}
        <div className="bg-[#4ECDC4] border-b-4 border-black p-6 flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-black text-black">SUBSCRIPTION SUPPORT</h2>
            <p className="text-sm font-bold text-gray-700 mt-1">
              Need help with your subscription?
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-black/10 rounded transition-colors"
            aria-label="Close"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Form */}
        <div className="p-6">
          {/* Success Message */}
          {submitStatus === 'success' && (
            <div className="bg-[#6BCF7F] border-4 border-black p-6 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
              <div className="flex items-center gap-3 mb-3">
                <div className="w-12 h-12 bg-white border-4 border-black rounded-full flex items-center justify-center">
                  <span className="text-2xl">✓</span>
                </div>
                <div>
                  <p className="font-black text-xl">MESSAGE SENT!</p>
                  <p className="font-bold text-sm">We'll respond within 24 hours</p>
                </div>
              </div>
            </div>
          )}

          {/* Error Message */}
          {submitStatus === 'error' && (
            <div className="bg-[#FF6B6B] border-4 border-black p-4 mb-4">
              <p className="font-black">Failed to send message. Please try again or email us directly at support@mirmer.ai</p>
            </div>
          )}

          {/* Show form only if not in success state */}
          {submitStatus !== 'success' && (
            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Name */}
              <div>
                <label className="block font-black text-sm mb-2">
                  NAME
                </label>
                <Input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                  className="w-full"
                  disabled
                />
              </div>

              {/* Email */}
              <div>
                <label className="block font-black text-sm mb-2">
                  EMAIL
                </label>
                <Input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  className="w-full"
                  disabled
                />
              </div>

              {/* Subject */}
              <div>
                <label className="block font-black text-sm mb-2">
                  SUBJECT <span className="text-[#FF6B6B]">*</span>
                </label>
                <select
                  name="subject"
                  value={formData.subject}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-3 border-4 border-black font-bold focus:outline-none focus:ring-4 focus:ring-[#4ECDC4]"
                >
                  <option value="">Select a topic</option>
                  <option value="cancel">Cancel Subscription</option>
                  <option value="billing">Billing Issue</option>
                  <option value="upgrade">Upgrade Plan</option>
                  <option value="refund">Request Refund</option>
                  <option value="other">Other</option>
                </select>
              </div>

              {/* Message */}
              <div>
                <label className="block font-black text-sm mb-2">
                  MESSAGE <span className="text-[#FF6B6B]">*</span>
                </label>
                <textarea
                  name="message"
                  value={formData.message}
                  onChange={handleChange}
                  required
                  rows={4}
                  placeholder="Describe your issue or question..."
                  className="w-full px-4 py-3 border-4 border-black font-bold focus:outline-none focus:ring-4 focus:ring-[#4ECDC4] resize-none"
                />
              </div>

              {/* Submit Button */}
              <div className="flex gap-4">
                <Button
                  type="submit"
                  disabled={isSubmitting}
                  className="flex-1 bg-[#4ECDC4] hover:bg-[#3dbdb3] font-black"
                >
                  {isSubmitting ? 'SENDING...' : 'SEND MESSAGE'}
                </Button>
                <Button
                  type="button"
                  onClick={onClose}
                  className="bg-gray-300 hover:bg-gray-400 text-black font-black"
                >
                  CANCEL
                </Button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  )
}
