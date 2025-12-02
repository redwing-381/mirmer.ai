#!/bin/bash
# Script to update domain URLs in the SDK

set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║          🌐 UPDATE DOMAIN URLs IN SDK                        ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Must run from sdk/ directory"
    exit 1
fi

# Get current URLs
echo "Current URLs:"
echo "  Auth: https://mirmer.ai"
echo "  API:  https://api.mirmer.ai"
echo ""

# Ask for new URLs
read -p "Enter your production domain (e.g., myapp.com): " domain

if [ -z "$domain" ]; then
    echo "❌ Error: Domain cannot be empty"
    exit 1
fi

# Construct URLs
auth_url="https://$domain"
api_url="https://api.$domain"

echo ""
echo "New URLs will be:"
echo "  Auth: $auth_url"
echo "  API:  $api_url"
echo ""

read -p "Continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "❌ Cancelled"
    exit 0
fi

echo ""
echo "🔄 Updating files..."

# Update client.py
sed -i.bak "s|base_url: str = \"https://api.mirmer.ai\"|base_url: str = \"$api_url\"|g" mirmer/client.py
echo "  ✓ Updated mirmer/client.py"

# Update async_client.py
sed -i.bak "s|base_url: str = \"https://api.mirmer.ai\"|base_url: str = \"$api_url\"|g" mirmer/async_client.py
echo "  ✓ Updated mirmer/async_client.py"

# Update auth.py
sed -i.bak "s|base_url: str = \"https://mirmer.ai\"|base_url: str = \"$auth_url\"|g" mirmer/auth.py
echo "  ✓ Updated mirmer/auth.py"

# Update cli.py
sed -i.bak "s|default=\"https://mirmer.ai\"|default=\"$auth_url\"|g" mirmer/cli.py
sed -i.bak "s|base_url.replace(\"https://mirmer.ai\", \"https://api.mirmer.ai\")|base_url.replace(\"$auth_url\", \"$api_url\")|g" mirmer/cli.py
echo "  ✓ Updated mirmer/cli.py"

# Update pyproject.toml URLs
sed -i.bak "s|Homepage = \"https://mirmer.ai\"|Homepage = \"$auth_url\"|g" pyproject.toml
sed -i.bak "s|Documentation = \"https://docs.mirmer.ai\"|Documentation = \"https://docs.$domain\"|g" pyproject.toml
echo "  ✓ Updated pyproject.toml"

# Clean up backup files
rm -f mirmer/*.bak pyproject.toml.bak

echo ""
echo "✅ URLs updated successfully!"
echo ""
echo "📝 Next steps:"
echo "  1. Review the changes: git diff"
echo "  2. Test locally: mirmer --help"
echo "  3. Rebuild package: rm -rf dist/ && uv build"
echo "  4. Publish: uv publish --token pypi-YOUR_TOKEN"
echo ""
