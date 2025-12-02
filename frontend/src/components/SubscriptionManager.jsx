import { useState, useEffect } from 'react'
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from './ui/Card'
import { Button } from './ui/Button'
import { Badge } from './ui/Badge'
import { Loader2, CreditCard, Calendar, AlertCircle, RefreshCw, Clock } from 'lucide-react'

export default function SubscriptionManager({ user, usageStats, onRefresh }) {
  const [subscription, setSubscription] = useState(null)
  const [loading, setLoading] = useState(true)
  const [actionLoading, setActionLoading] = useState(false)
  const [syncing, setSyncing] = useState(false)
  const [error, setError] = useState(null)
  const [lastSyncTime, setLastSyncTime] = useState(null)

  useEffect(() => {
    fetchSubscription()
  }, [])

  // Update subscription when usageStats changes
  useEffect(() => {
    if (usageStats) {
      setSubscription(prev => ({
        ...prev,
        tier: usageStats.tier,
        status: usageStats.subscription_status,
        subscription_id: usageStats.subscription_id
      }))
    }
  }, [usageStats])

  const fetchSubscription = async () => {
    try {
      const idToken = await user.getIdToken()
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/payments/subscription`, {
        headers: {
          'Authorization': `Bearer ${idToken}`,
          'X-User-Id': user.uid
        }
      })

      if (!response.ok) {
        throw new Error('Failed to fetch subscription')
      }

      const data = await response.json()
      setSubscription(data)
      setLastSyncTime(new Date())
    } catch (err) {
      console.error('Error fetching subscription:', err)
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleSyncSubscription = async () => {
    setSyncing(true)
    setError(null)

    try {
      const idToken = await user.getIdToken()
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/payments/verify-subscription`, {
        headers: {
          'Authorization': `Bearer ${idToken}`,
          'X-User-Id': user.uid
        }
      })

      if (!response.ok) {
        throw new Error('Failed to sync subscription')
      }

      const result = await response.json()
      
      // Update subscription data
      await fetchSubscription()
      setLastSyncTime(new Date())
      
      // Notify parent to refresh usage stats
      if (onRefresh) {
        await onRefresh()
      }
    } catch (err) {
      console.error('Sync error:', err)
      setError(err.message)
    } finally {
      setSyncing(false)
    }
  }

  const handleCancelSubscription = async () => {
    if (!window.confirm('Are you sure you want to cancel your Pro subscription? You will lose access to Pro features at the end of the current billing period.')) {
      return
    }

    setActionLoading(true)
    setError(null)

    try {
      const idToken = await user.getIdToken()
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/payments/cancel-subscription`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${idToken}`,
          'X-User-Id': user.uid
        }
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to cancel subscription')
      }

      // Refresh subscription info
      await fetchSubscription()
      alert('Subscription cancelled successfully')
    } catch (err) {
      console.error('Cancel error:', err)
      setError(err.message)
    } finally {
      setActionLoading(false)
    }
  }

  if (loading) {
    return (
      <Card>
        <CardContent className="flex items-center justify-center py-12">
          <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
        </CardContent>
      </Card>
    )
  }

  const formatDate = (timestamp) => {
    if (!timestamp) return 'N/A'
    return new Date(timestamp * 1000).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }

  const getStatusBadge = (status) => {
    const variants = {
      active: 'success',
      canceled: 'default',
      past_due: 'warning',
      unpaid: 'danger'
    }
    return variants[status] || 'default'
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <CardTitle>Subscription</CardTitle>
            <CardDescription>Manage your billing and subscription</CardDescription>
          </div>
          <div className="flex items-center gap-3">
            {subscription?.tier && (
              <Badge variant={subscription.tier === 'pro' ? 'success' : 'default'}>
                {subscription.tier.toUpperCase()}
              </Badge>
            )}
            <Button
              variant="outline"
              size="sm"
              onClick={handleSyncSubscription}
              disabled={syncing}
              className="flex items-center gap-2"
            >
              <RefreshCw className={`w-4 h-4 ${syncing ? 'animate-spin' : ''}`} />
              {syncing ? 'Syncing...' : 'Sync'}
            </Button>
          </div>
        </div>
        {lastSyncTime && (
          <div className="flex items-center gap-2 mt-2 text-xs text-gray-500">
            <Clock className="w-3 h-3" />
            <span>Last synced: {lastSyncTime.toLocaleTimeString()}</span>
          </div>
        )}
      </CardHeader>

      <CardContent className="space-y-4">
        {error && (
          <div className="p-4 bg-red-50 border-4 border-red-500 rounded-lg flex items-start">
            <AlertCircle className="w-5 h-5 text-red-500 mr-3 flex-shrink-0 mt-0.5" />
            <p className="text-red-700 font-bold">{error}</p>
          </div>
        )}

        {/* Usage Limits - Always show */}
        {usageStats && (
          <div className="space-y-3 p-4 bg-gray-50 border-2 border-gray-200 rounded-lg">
            <h4 className="font-bold text-sm text-gray-700">Query Limits</h4>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-xs text-gray-500 mb-1">Daily Limit</p>
                <p className="text-lg font-black">{usageStats.daily_limit}</p>
              </div>
              <div>
                <p className="text-xs text-gray-500 mb-1">Monthly Limit</p>
                <p className="text-lg font-black">{usageStats.monthly_limit}</p>
              </div>
            </div>
          </div>
        )}

        {subscription?.tier === 'free' ? (
          <div className="text-center py-6">
            <p className="text-gray-600 mb-4">You're currently on the Free plan</p>
            <p className="text-sm text-gray-500">Upgrade to Pro for more queries and features</p>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="flex items-center justify-between py-3 border-b-2 border-gray-200">
              <div className="flex items-center">
                <CreditCard className="w-5 h-5 text-gray-400 mr-3" />
                <span className="font-bold">Status</span>
              </div>
              <Badge variant={getStatusBadge(subscription?.status)}>
                {subscription?.status?.toUpperCase() || 'UNKNOWN'}
              </Badge>
            </div>

            {subscription?.current_period_end && (
              <div className="flex items-center justify-between py-3 border-b-2 border-gray-200">
                <div className="flex items-center">
                  <Calendar className="w-5 h-5 text-gray-400 mr-3" />
                  <span className="font-bold">
                    {subscription?.cancel_at_period_end ? 'Expires on' : 'Renews on'}
                  </span>
                </div>
                <span className="text-gray-700">
                  {formatDate(subscription.current_period_end)}
                </span>
              </div>
            )}

            {subscription?.cancel_at_period_end && (
              <div className="p-4 bg-yellow-50 border-4 border-yellow-400 rounded-lg">
                <p className="text-sm text-gray-700">
                  <strong>Your subscription will be canceled</strong> at the end of the current billing period.
                  You'll still have access to Pro features until then.
                </p>
              </div>
            )}
          </div>
        )}
      </CardContent>

      {subscription?.tier === 'pro' && subscription?.status === 'active' && (
        <CardFooter>
          <Button
            className="w-full"
            variant="danger"
            onClick={handleCancelSubscription}
            disabled={actionLoading}
          >
            {actionLoading ? (
              <>
                <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                Cancelling...
              </>
            ) : (
              'Cancel Subscription'
            )}
          </Button>
        </CardFooter>
      )}
    </Card>
  )
}
