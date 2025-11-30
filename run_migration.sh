#!/bin/bash

# Script to run database migration for subscription fields
# Usage: ./run_migration.sh <railway-url> <admin-key>

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: ./run_migration.sh <railway-url> <admin-key>"
    echo "Example: ./run_migration.sh https://your-app.railway.app your-secret-key"
    exit 1
fi

RAILWAY_URL=$1
ADMIN_KEY=$2

echo "🔧 Running database migration..."
echo "URL: $RAILWAY_URL"
echo ""

response=$(curl -s -X POST "$RAILWAY_URL/api/admin/migrate-subscription-fields" \
  -H "X-Admin-Key: $ADMIN_KEY" \
  -w "\nHTTP_STATUS:%{http_code}")

http_status=$(echo "$response" | grep "HTTP_STATUS" | cut -d: -f2)
body=$(echo "$response" | grep -v "HTTP_STATUS")

echo "Response: $body"
echo "Status: $http_status"
echo ""

if [ "$http_status" = "200" ]; then
    echo "✅ Migration completed successfully!"
else
    echo "❌ Migration failed with status $http_status"
    exit 1
fi
