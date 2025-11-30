import { useState, useEffect } from 'react'

/**
 * Usage Statistics Component
 * Displays user's query usage and limits
 */
export default function UsageStats({ userId }) {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (userId) {
      loadStats()
    }
  }, [userId])

  const loadStats = async () => {
    try {
      const response = await fetch('/api/usage', {
        headers: {
          'X-User-Id': userId,
        },
      })
      const data = await response.json()
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
    <div className="bg-white border border-gray-200 rounded-lg p-4 mb-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-semibold text-gray-900">Usage</h3>
        <span className={`px-2 py-1 text-xs font-medium rounded-full ${
          stats.tier === 'free' 
            ? 'bg-gray-100 text-gray-700' 
            : 'bg-blue-100 text-blue-700'
        }`}>
          {stats.tier.toUpperCase()}
        </span>
      </div>

      {stats.tier === 'free' && (
        <>
          {/* Daily Usage */}
          <div className="mb-3">
            <div className="flex justify-between text-sm mb-1">
              <span className="text-gray-600">Today</span>
              <span className="font-medium text-gray-900">
                {stats.daily_used} / {stats.daily_limit}
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className={`h-2 rounded-full transition-all ${
                  dailyPercent >= 80 ? 'bg-red-500' : 'bg-blue-500'
                }`}
                style={{ width: `${Math.min(dailyPercent, 100)}%` }}
              />
            </div>
          </div>

          {/* Monthly Usage */}
          <div className="mb-3">
            <div className="flex justify-between text-sm mb-1">
              <span className="text-gray-600">This Month</span>
              <span className="font-medium text-gray-900">
                {stats.monthly_used} / {stats.monthly_limit}
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className={`h-2 rounded-full transition-all ${
                  monthlyPercent >= 80 ? 'bg-red-500' : 'bg-green-500'
                }`}
                style={{ width: `${Math.min(monthlyPercent, 100)}%` }}
              />
            </div>
          </div>

          {/* Upgrade CTA */}
          {(dailyPercent >= 70 || monthlyPercent >= 70) && (
            <div className="mt-3 p-3 bg-blue-50 rounded-lg">
              <p className="text-sm text-blue-900 mb-2">
                Running low on queries?
              </p>
              <button className="text-sm font-medium text-blue-600 hover:text-blue-700">
                Upgrade to Pro →
              </button>
            </div>
          )}
        </>
      )}

      {stats.tier !== 'free' && (
        <div className="text-sm text-gray-600">
          <p>✨ Unlimited queries</p>
          <p className="text-xs mt-1">Total: {stats.total_queries} queries</p>
        </div>
      )}
    </div>
  )
}
