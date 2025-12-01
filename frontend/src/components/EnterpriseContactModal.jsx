import { useState } from 'react'
import { X } from 'lucide-react'
import { Button } from './ui/Button'
import { Input } from './ui/Input'

export default function EnterpriseContactModal({ isOpen, onClose }) {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    company: '',
    companySize: '',
    phone: '',
    message: '',
    useCase: ''
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
      const response = await fetch('/api/enterprise/contact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      })

      if (response.ok) {
        setSubmitStatus('success')
        // Reset form
        setFormData({
          name: '',
          email: '',
          company: '',
          companySize: '',
          phone: '',
          message: '',
          useCase: ''
        })
        // Close modal after 5 seconds to let user see the success message
        setTimeout(() => {
          onClose()
          setSubmitStatus(null)
        }, 5000)
      } else {
        setSubmitStatus('error')
      }
    } catch (error) {
      console.error('Error submitting form:', error)
      setSubmitStatus('error')
    } finally {
      setIsSubmitting(false)
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
      <div className="relative w-full max-w-2xl bg-white border-4 border-black shadow-[12px_12px_0px_0px_rgba(0,0,0,1)] max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-[#FFE66D] border-b-4 border-black p-6 flex justify-between items-center">
          <div>
            <h2 className="text-3xl font-black text-black">CONTACT ENTERPRISE SALES</h2>
            <p className="text-sm font-bold text-gray-700 mt-1">
              Let's discuss how Mirmer AI can help your organization
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
            <div className="bg-[#6BCF7F] border-4 border-black p-6 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] animate-pulse">
              <div className="flex items-center gap-3 mb-3">
                <div className="w-12 h-12 bg-white border-4 border-black rounded-full flex items-center justify-center">
                  <span className="text-2xl">✓</span>
                </div>
                <div>
                  <p className="font-black text-2xl">MESSAGE SENT!</p>
                  <p className="font-bold text-sm">Check your email for confirmation</p>
                </div>
              </div>
              <div className="bg-white border-4 border-black p-4 mt-4">
                <p className="font-black text-sm mb-2">WHAT HAPPENS NEXT?</p>
                <ul className="space-y-1 text-sm font-bold">
                  <li>✓ You'll receive a confirmation email</li>
                  <li>✓ Our team will review your inquiry</li>
                  <li>✓ We'll contact you within 1-2 business days</li>
                </ul>
              </div>
              <p className="text-center font-black text-sm mt-4 text-gray-700">
                This window will close automatically in 5 seconds...
              </p>
            </div>
          )}

          {/* Error Message */}
          {submitStatus === 'error' && (
            <div className="bg-[#FF6B6B] border-4 border-black p-6 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
              <div className="flex items-center gap-3 mb-3">
                <div className="w-12 h-12 bg-white border-4 border-black rounded-full flex items-center justify-center">
                  <span className="text-2xl">✗</span>
                </div>
                <div>
                  <p className="font-black text-2xl">OOPS!</p>
                  <p className="font-bold text-sm">Something went wrong</p>
                </div>
              </div>
              <div className="bg-white border-4 border-black p-4 mt-4">
                <p className="font-bold text-sm mb-2">Please try again or contact us directly:</p>
                <p className="font-black text-sm">📧 solaimuthu006@gmail.com</p>
              </div>
            </div>
          )}

          {/* Show form only if not in success state */}
          {submitStatus !== 'success' && (
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Name */}
              <div>
            <label className="block font-black text-sm mb-2">
              NAME <span className="text-[#FF6B6B]">*</span>
            </label>
            <Input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              placeholder="John Doe"
              className="w-full"
            />
          </div>

          {/* Email */}
          <div>
            <label className="block font-black text-sm mb-2">
              EMAIL <span className="text-[#FF6B6B]">*</span>
            </label>
            <Input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              placeholder="john@company.com"
              className="w-full"
            />
          </div>

          {/* Company */}
          <div>
            <label className="block font-black text-sm mb-2">
              COMPANY <span className="text-[#FF6B6B]">*</span>
            </label>
            <Input
              type="text"
              name="company"
              value={formData.company}
              onChange={handleChange}
              required
              placeholder="Acme Corp"
              className="w-full"
            />
          </div>

          {/* Company Size */}
          <div>
            <label className="block font-black text-sm mb-2">
              COMPANY SIZE <span className="text-[#FF6B6B]">*</span>
            </label>
            <select
              name="companySize"
              value={formData.companySize}
              onChange={handleChange}
              required
              className="w-full px-4 py-3 border-4 border-black font-bold focus:outline-none focus:ring-4 focus:ring-[#4ECDC4]"
            >
              <option value="">Select size</option>
              <option value="1-10">1-10 employees</option>
              <option value="11-50">11-50 employees</option>
              <option value="51-200">51-200 employees</option>
              <option value="201-1000">201-1000 employees</option>
              <option value="1000+">1000+ employees</option>
            </select>
          </div>

          {/* Phone (Optional) */}
          <div>
            <label className="block font-black text-sm mb-2">
              PHONE (OPTIONAL)
            </label>
            <Input
              type="tel"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              placeholder="+1 (555) 123-4567"
              className="w-full"
            />
          </div>

          {/* Use Case (Optional) */}
          <div>
            <label className="block font-black text-sm mb-2">
              USE CASE (OPTIONAL)
            </label>
            <Input
              type="text"
              name="useCase"
              value={formData.useCase}
              onChange={handleChange}
              placeholder="e.g., Customer support, Research, Content creation"
              className="w-full"
            />
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
              placeholder="Tell us about your needs..."
              className="w-full px-4 py-3 border-4 border-black font-bold focus:outline-none focus:ring-4 focus:ring-[#4ECDC4] resize-none"
            />
          </div>

          {/* Submit Button */}
          <div className="flex gap-4">
            <Button
              type="submit"
              disabled={isSubmitting}
              className="flex-1 bg-[#4ECDC4] hover:bg-[#3dbdb3] font-black text-lg"
            >
              {isSubmitting ? 'SENDING...' : 'SEND MESSAGE'}
            </Button>
            <Button
              type="button"
              onClick={onClose}
              className="bg-gray-300 hover:bg-gray-400 text-black font-black text-lg"
            >
              CANCEL
            </Button>
          </div>

              {/* Privacy Note */}
              <p className="text-xs text-gray-600 font-bold text-center">
                By submitting this form, you agree to be contacted by our sales team.
              </p>
            </form>
          )}
        </div>
      </div>
    </div>
  )
}
