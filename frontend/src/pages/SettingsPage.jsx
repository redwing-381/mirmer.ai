import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import { Button } from '../components/ui/Button'
import SubscriptionManager from '../components/SubscriptionManager'
import UsageStats from '../components/UsageStats'

export default function SettingsPage({ user }) {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      {/* Header */}
      <div className="bg-white border-b-4 border-black">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Button
                variant="ghost"
                onClick={() => navigate('/app')}
                className="flex items-center"
              >
                <ArrowLeft className="w-5 h-5 mr-2" />
                Back to Chat
              </Button>
              <h1 className="text-2xl font-black">Settings</h1>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Subscription Management */}
          <div>
            <SubscriptionManager user={user} />
          </div>

          {/* Usage Stats */}
          <div>
            <UsageStats userId={user?.uid} user={user} />
          </div>

          {/* Account Info */}
          <div className="md:col-span-2">
            <div className="bg-white border-4 border-black rounded-lg p-6">
              <h2 className="text-xl font-black mb-4">Account Information</h2>
              <div className="space-y-3">
                <div className="flex justify-between py-2 border-b-2 border-gray-200">
                  <span className="font-bold text-gray-600">Email</span>
                  <span className="text-gray-900">{user?.email}</span>
                </div>
                <div className="flex justify-between py-2 border-b-2 border-gray-200">
                  <span className="font-bold text-gray-600">User ID</span>
                  <span className="text-gray-900 text-sm font-mono">{user?.uid}</span>
                </div>
                <div className="flex justify-between py-2">
                  <span className="font-bold text-gray-600">Account Created</span>
                  <span className="text-gray-900">
                    {user?.metadata?.creationTime 
                      ? new Date(user.metadata.creationTime).toLocaleDateString()
                      : 'N/A'}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
