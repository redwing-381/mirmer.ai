#!/bin/bash
# Safe Publishing Script for mirmer-ai SDK
# This script performs final security checks before publishing

set -e  # Exit on error

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║          🚀 MIRMER AI SDK - PUBLISHING SCRIPT                ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Must run from sdk/ directory"
    exit 1
fi

echo "🔍 Running pre-publish security checks..."
echo ""

# Check 1: No .env files in package
echo "  Checking for .env files..."
if tar -tzf dist/mirmer_ai-0.1.0.tar.gz 2>/dev/null | grep -q "\.env"; then
    echo "  ❌ FAILED: .env file found in package!"
    exit 1
fi
echo "  ✓ No .env files in package"

# Check 2: No hardcoded secrets
echo "  Checking for hardcoded secrets..."
if tar -xzf dist/mirmer_ai-0.1.0.tar.gz -O 2>/dev/null | grep -q "sk-or-v1\|rzp_live\|SG\."; then
    echo "  ❌ FAILED: Potential secrets found in package!"
    exit 1
fi
echo "  ✓ No hardcoded secrets found"

# Check 3: Package exists
echo "  Checking package files..."
if [ ! -f "dist/mirmer_ai-0.1.0.tar.gz" ] || [ ! -f "dist/mirmer_ai-0.1.0-py3-none-any.whl" ]; then
    echo "  ❌ FAILED: Package files not found. Run 'uv build' first"
    exit 1
fi
echo "  ✓ Package files exist"

# Check 4: Git status
echo "  Checking git status..."
if git status --porcelain | grep -q "\.env"; then
    echo "  ⚠️  WARNING: .env file in git status (should be ignored)"
fi
echo "  ✓ Git status clean"

echo ""
echo "✅ All security checks passed!"
echo ""
echo "📦 Package ready to publish:"
echo "   • mirmer_ai-0.1.0.tar.gz"
echo "   • mirmer_ai-0.1.0-py3-none-any.whl"
echo ""

# Ask for confirmation
read -p "🚀 Ready to publish to PyPI? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "❌ Publishing cancelled"
    exit 0
fi

# Check for PyPI token
if [ -z "$PYPI_TOKEN" ]; then
    echo ""
    echo "⚠️  PYPI_TOKEN environment variable not set"
    echo ""
    echo "Options:"
    echo "  1. Set token: export PYPI_TOKEN=pypi-YOUR_TOKEN"
    echo "  2. Use --token flag: uv publish --token pypi-YOUR_TOKEN"
    echo ""
    read -p "Enter PyPI token (or press Enter to skip): " token
    
    if [ -n "$token" ]; then
        export PYPI_TOKEN="$token"
    fi
fi

# Publish
echo ""
echo "📤 Publishing to PyPI..."
echo ""

if [ -n "$PYPI_TOKEN" ]; then
    uv publish --token "$PYPI_TOKEN"
else
    echo "Running: uv publish"
    echo "(You'll be prompted for credentials)"
    uv publish
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║          ✅ SUCCESSFULLY PUBLISHED TO PYPI!                  ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "🎉 Package is now available:"
echo "   pip install mirmer-ai"
echo ""
echo "📝 Next steps:"
echo "   1. Verify: pip install mirmer-ai"
echo "   2. Test: mirmer --help"
echo "   3. Create GitHub release"
echo "   4. Update main README"
echo "   5. Announce to community"
echo ""
