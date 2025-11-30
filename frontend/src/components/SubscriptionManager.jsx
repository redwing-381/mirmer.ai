import { useState, useEffect } from 'react'
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from './ui/Card'
import { Button } from './ui/Button'
import { Badge } from './ui/Badge'
import { Loader2, CreditCard, Calendar, AlertCircle } from 'lucide-react'

export default function SubscriptionManager({ user }) {
  const [subscription, setSubscription] = useState(null)
  const [loading, setLoading] = useState(true)
  const [actionLoading, setActionLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchSubscription()
  }, [])

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
    } catch (err) {
      console.error('Error fetching subscription:', err)
      setError(err.message)
    } finally {
      setLoading(false)
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
          <div>
            <CardTitle>Subscription</CardTitle>
            <CardDescription>Manage your billing and subscription</CardDescription>
          </div>
          {subscription?.tier && (
            <Badge variant={subscription.tier === 'pro' ? 'success' : 'default'}>
              {subscription.tier.toUpperCase()}
            </Badge>
          )}
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        {error && (
          <div className="p-4 bg-red-50 border-4 border-red-500 rounded-lg flex items-start">
            <AlertCircle className="w-5 h-5 text-red-500 mr-3 flex-shrink-0 mt-0.5" />
            <p className="text-red-700 font-bold">{error}</p>
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
