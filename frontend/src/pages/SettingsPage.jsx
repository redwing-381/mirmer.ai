import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { auth, logout } from '../firebase'
import { onAuthStateChanged } from 'firebase/auth'
import { api } from '../api'
import UpgradeModal from '../components/UpgradeModal'
import { ArrowLeft } from 'lucide-react'

export default function SettingsPage() {
  const navigate = useNavigate()
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [usageStats, setUsageStats] = useState(null)
  const [showUpgradeModal, setShowUpgradeModal] = useState(false)

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser)
      setLoading(false)
      
      if (!currentUser) {
        navigate('/')
      }
    })
    return () => unsubscribe()
  }, [navigate])

  useEffect(() => {
    if (user) {
      loadUsageStats()
    }
  }, [user])

  const loadUsageStats = async () => {
    if (!user) return
    try {
      const stats = await api.getUsageStats(user.uid)
      setUsageStats(stats)
    } catch (error) {
      console.error('Error loading usage stats:', error)
    }
  }

  const handleLogout = async () => {
    try {
      await logout()
      navigate('/')
    } catch (error) {
      console.error('Error logging out:', error)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-[#f5f5f5] flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-4 border-black"></div>
      </div>
    )
  }

  const isPro = usageStats?.tier === 'pro'

  return (
    <div className="min-h-screen bg-[#f5f5f5]" style={{
      backgroundImage: `
        linear-gradient(rgba(0, 0, 0, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 0, 0, 0.03) 1px, transparent 1px)
      `,
      backgroundSize: '20px 20px'
    }}>
      {/* Header */}
      <div className="bg-white border-b-4 border-black p-6">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <button
              onClick={() => navigate('/app')}
              className="p-2 border-4 border-black bg-white shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[-2px] hover:translate-y-[-2px] transition-all"
            >
              <ArrowLeft className="w-6 h-6" />
            </button>
            <h1 className="text-4xl font-black">SETTINGS</h1>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-4xl mx-auto p-6 space-y-6">
        {/* Account Section */}
        <div className="bg-white border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] p-8">
          <h2 className="text-2xl font-black mb-6">ACCOUNT</h2>
          
          <div className="space-y-4">
            <div className="flex items-center space-x-4">
              <img 
                src={user?.photoURL} 
                alt={user?.displayName}
                className="w-16 h-16 border-4 border-black"
              />
              <div>
                <p className="font-black text-lg">{user?.displayName}</p>
                <p className="font-bold text-gray-600">{user?.email}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Subscription Section */}
        <div className="bg-white border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] p-8">
          <h2 className="text-2xl font-black mb-6">SUBSCRIPTION</h2>
          
          <div className="space-y-6">
            {/* Current Plan */}
            <div className={`p-6 border-4 border-black ${isPro ? 'bg-[#FFE66D]' : 'bg-[#f5f5f5]'}`}>
              <div className="flex items-center justify-between mb-4">
                <div>
                  <p className="text-sm font-black text-gray-600">CURRENT PLAN</p>
                  <p className="text-3xl font-black">{isPro ? 'PRO' : 'FREE'}</p>
                </div>
                {isPro && (
                  <div className="px-4 py-2 bg-[#4ECDC4] border-4 border-black font-black">
                    ACTIVE
                  </div>
                )}
              </div>
              
              <div className="space-y-2">
                <p className="font-bold">
                  <span className="text-gray-600">Daily Limit:</span> {usageStats?.daily_limit || 10} queries
                </p>
                <p className="font-bold">
                  <span className="text-gray-600">Monthly Limit:</span> {usageStats?.monthly_limit || 300} queries
                </p>
                <p className="font-bold">
                  <span className="text-gray-600">Used Today:</span> {usageStats?.daily_queries_used || 0} / {usageStats?.daily_limit || 10}
                </p>
              </div>
            </div>

            {/* Upgrade Button for Free Users */}
            {!isPro && (
              <div className="p-6 bg-[#4ECDC4] border-4 border-black">
                <h3 className="text-xl font-black mb-3">UPGRADE TO PRO</h3>
                <ul className="space-y-2 mb-4">
                  <li className="flex items-start">
                    <span className="text-black mr-2 font-black">✓</span>
                    <span className="font-bold">100 queries per day (10x more!)</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-black mr-2 font-black">✓</span>
                    <span className="font-bold">Priority processing</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-black mr-2 font-black">✓</span>
                    <span className="font-bold">Extended history (90 days)</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-black mr-2 font-black">✓</span>
                    <span className="font-bold">Email support</span>
                  </li>
                </ul>
                <button
                  onClick={() => setShowUpgradeModal(true)}
                  className="w-full px-6 py-3 bg-[#FF6B6B] text-white border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[-2px] hover:translate-y-[-2px] active:shadow-none active:translate-x-1 active:translate-y-1 transition-all font-black text-lg"
                >
                  UPGRADE NOW - ₹1499/MONTH
                </button>
              </div>
            )}

            {/* Manage Subscription for Pro Users */}
            {isPro && (
              <div className="p-6 bg-[#f5f5f5] border-4 border-black">
                <h3 className="text-xl font-black mb-3">MANAGE SUBSCRIPTION</h3>
                <p className="font-bold text-gray-600 mb-4">
                  Your Pro subscription is active. Contact support to manage your subscription.
                </p>
                <a
                  href="mailto:support@mirmer.ai?subject=Subscription Management"
                  className="inline-block px-6 py-2 bg-white border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[-2px] hover:translate-y-[-2px] transition-all font-black"
                >
                  CONTACT SUPPORT
                </a>
              </div>
            )}
          </div>
        </div>

        {/* Danger Zone */}
        <div className="bg-white border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] p-8">
          <h2 className="text-2xl font-black mb-6 text-[#FF6B6B]">DANGER ZONE</h2>
          
          <div className="space-y-4">
            <button
              onClick={handleLogout}
              className="px-6 py-2 bg-white border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[-2px] hover:translate-y-[-2px] transition-all font-black"
            >
              LOGOUT
            </button>
          </div>
        </div>
      </div>

      {/* Upgrade Modal */}
      <UpgradeModal 
        isOpen={showUpgradeModal} 
        onClose={() => setShowUpgradeModal(false)} 
      />
    </div>
  )
}
