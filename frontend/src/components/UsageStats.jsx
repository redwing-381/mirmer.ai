import { useState, useEffect } from 'react'
import { api } from '../api'
import UpgradeModal from './UpgradeModal'

/**
 * Usage Statistics Component
 * Displays user's query usage and limits
 */
export default function UsageStats({ userId, user }) {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [showUpgradeModal, setShowUpgradeModal] = useState(false)

  useEffect(() => {
    if (userId) {
      loadStats()
    }
  }, [userId])

  const loadStats = async () => {
    try {
      const data = await api.getUsageStats(userId)
      setStats(data)
    } catch (error) {
      console.error('Error loading usage stats:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading || !stats) return null

  const dailyPercent = stats.daily_limit === 'unlimited' 
    ? 0 
    : (stats.daily_used / stats.daily_limit) * 100

  const monthlyPercent = stats.monthly_limit === 'unlimited'
    ? 0
    : (stats.monthly_used / stats.monthly_limit) * 100

  return (
    <div className="bg-white border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] p-4">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-black text-lg">USAGE</h3>
        <span className={`px-3 py-1 text-xs font-black border-2 border-black ${
          stats.tier === 'free' 
            ? 'bg-gray-200 text-black' 
            : 'bg-[#4ECDC4] text-black'
        }`}>
          {stats.tier.toUpperCase()}
        </span>
      </div>

      {stats.tier === 'free' && (
        <>
          {/* Daily Usage */}
          <div className="mb-4">
            <div className="flex justify-between text-sm mb-2">
              <span className="font-bold">Today</span>
              <span className="font-black">
                {stats.daily_used} / {stats.daily_limit}
              </span>
            </div>
            <div className="w-full bg-gray-200 border-2 border-black h-4">
              <div
                className={`h-full transition-all ${
                  dailyPercent >= 80 ? 'bg-[#FF6B6B]' : 'bg-[#4ECDC4]'
                }`}
                style={{ width: `${Math.min(dailyPercent, 100)}%` }}
              />
            </div>
          </div>

          {/* Monthly Usage */}
          <div className="mb-4">
            <div className="flex justify-between text-sm mb-2">
              <span className="font-bold">This Month</span>
              <span className="font-black">
                {stats.monthly_used} / {stats.monthly_limit}
              </span>
            </div>
            <div className="w-full bg-gray-200 border-2 border-black h-4">
              <div
                className={`h-full transition-all ${
                  monthlyPercent >= 80 ? 'bg-[#FF6B6B]' : 'bg-[#FFE66D]'
                }`}
                style={{ width: `${Math.min(monthlyPercent, 100)}%` }}
              />
            </div>
          </div>

          {/* Upgrade CTA */}
          {(dailyPercent >= 70 || monthlyPercent >= 70) && (
            <div className="mt-3 p-3 bg-[#FFE66D] border-4 border-black shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]">
              <p className="text-sm font-black mb-2">
                Running low on queries?
              </p>
              <button 
                onClick={() => setShowUpgradeModal(true)}
                className="text-sm font-black text-[#FF6B6B] hover:underline"
              >
                Upgrade to Pro →
              </button>
            </div>
          )}
        </>
      )}

      {stats.tier !== 'free' && (
        <div className="text-sm">
          <p className="font-black">Pro Plan Active</p>
          <p className="text-xs mt-1 font-bold">Total: {stats.total_queries} queries</p>
        </div>
      )}

      <UpgradeModal
        isOpen={showUpgradeModal}
        onClose={() => setShowUpgradeModal(false)}
        userEmail={user?.email}
        userId={user?.uid}
      />
    </div>
  )
}
