#!/bin/bash

# Simplified test script to verify critical fixes

echo "🧪 Testing Critical Fixes (File-based checks)..."
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Check file structure
echo "1️⃣  Checking file structure..."

files_to_check=(
    "backend/main.py"
    "backend/storage.py"
    "backend/usage.py"
    "backend/database.py"
    "backend/storage_postgres.py"
    "backend/usage_postgres.py"
    "backend/models.py"
    "backend/council.py"
)

all_files_exist=true
for file in "${files_to_check[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo -e "  ${RED}✗ $file missing${NC}"
        all_files_exist=false
    fi
done

if [ "$all_files_exist" = true ]; then
    echo -e "${GREEN}✓ All required files present${NC}"
else
    echo -e "${RED}✗ Some files are missing${NC}"
    exit 1
fi

echo ""

# Test 2: Check for proper imports in key files
echo "2️⃣  Checking import statements..."

check_import() {
    local file=$1
    local pattern=$2
    local description=$3
    
    if grep -q "$pattern" "$file"; then
        echo "  ✓ $description"
        return 0
    else
        echo -e "  ${RED}✗ $description${NC}"
        return 1
    fi
}

all_imports_correct=true

check_import "backend/storage.py" "from backend.storage_postgres import" "storage.py uses backend.storage_postgres" || all_imports_correct=false
check_import "backend/usage.py" "from backend.usage_postgres import" "usage.py uses backend.usage_postgres" || all_imports_correct=false
check_import "backend/main.py" "from backend import storage" "main.py imports backend.storage" || all_imports_correct=false
check_import "backend/main.py" "from backend import usage" "main.py imports backend.usage" || all_imports_correct=false
check_import "backend/storage_postgres.py" "from backend.database import" "storage_postgres.py imports backend.database" || all_imports_correct=false
check_import "backend/usage_postgres.py" "from backend.database import" "usage_postgres.py imports backend.database" || all_imports_correct=false
check_import "backend/database.py" "from backend import models" "database.py imports backend.models" || all_imports_correct=false
check_import "backend/payments.py" "from backend.models import" "payments.py imports backend.models" || all_imports_correct=false
check_import "backend/council.py" "from backend.openrouter import" "council.py imports backend.openrouter" || all_imports_correct=false
check_import "backend/openrouter.py" "from backend.config import" "openrouter.py imports backend.config" || all_imports_correct=false
check_import "backend/storage_json.py" "from backend.config import" "storage_json.py imports backend.config" || all_imports_correct=false

if [ "$all_imports_correct" = true ]; then
    echo -e "${GREEN}✓ All imports are correct${NC}"
else
    echo -e "${RED}✗ Some imports need fixing${NC}"
    exit 1
fi

echo ""

# Test 3: Check for frontend serving in main.py
echo "3️⃣  Checking frontend serving configuration..."

if grep -q "from fastapi.staticfiles import StaticFiles" "backend/main.py"; then
    echo "  ✓ StaticFiles import found"
else
    echo -e "  ${RED}✗ StaticFiles import missing${NC}"
    exit 1
fi

if grep -q "from fastapi.responses import FileResponse" "backend/main.py"; then
    echo "  ✓ FileResponse import found"
else
    echo -e "  ${RED}✗ FileResponse import missing${NC}"
    exit 1
fi

if grep -q 'app.mount.*assets.*StaticFiles' "backend/main.py"; then
    echo "  ✓ Assets mounting configured"
else
    echo -e "  ${RED}✗ Assets mounting not configured${NC}"
    exit 1
fi

if grep -q 'full_path:path' "backend/main.py"; then
    echo "  ✓ Catch-all route for SPA found"
else
    echo -e "  ${RED}✗ Catch-all route missing${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Frontend serving configured correctly${NC}"
echo ""

# Test 4: Check for production validation
echo "4️⃣  Checking production validation..."

if grep -q "IS_PRODUCTION = os.getenv('RAILWAY_ENVIRONMENT')" "backend/main.py"; then
    echo "  ✓ Production environment detection"
else
    echo -e "  ${YELLOW}⚠ Production environment detection not found${NC}"
fi

if grep -q "DATABASE_URL environment variable is required in production" "backend/main.py"; then
    echo "  ✓ DATABASE_URL validation in production"
else
    echo -e "  ${RED}✗ DATABASE_URL validation missing${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Production validation configured${NC}"
echo ""

# Test 5: Check environment variables
echo "5️⃣  Checking environment variables..."

if [ -f ".env" ]; then
    echo "✓ .env file found"
    
    # Check for critical variables
    if grep -q "OPENROUTER_API_KEY" .env; then
        echo "  ✓ OPENROUTER_API_KEY present"
    else
        echo -e "  ${YELLOW}⚠ OPENROUTER_API_KEY missing${NC}"
    fi
    
    if grep -q "DATABASE_URL" .env; then
        echo "  ✓ DATABASE_URL present (will use PostgreSQL)"
    else
        echo -e "  ${YELLOW}⚠ DATABASE_URL missing (will use JSON storage in dev)${NC}"
    fi
else
    echo -e "${YELLOW}⚠ .env file not found${NC}"
fi

echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ All file-based tests passed!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ Fixed Issues:"
echo "  1. Import statements now use 'backend.' prefix"
echo "  2. Frontend serving configured with StaticFiles"
echo "  3. Catch-all route added for SPA routing"
echo "  4. Production validation for DATABASE_URL"
echo ""
echo "📋 Next steps:"
echo "  1. Build frontend: cd frontend && npm run build"
echo "  2. Commit changes: git add . && git commit -m 'Fix: 404 errors, usage tracking, PostgreSQL enforcement'"
echo "  3. Push to Railway: git push"
echo "  4. Monitor deployment logs"
echo "  5. Test the deployed application"
echo ""
echo "📖 See DEPLOYMENT_GUIDE.md for detailed instructions."
echo "📝 See CRITICAL_FIXES_APPLIED.md for fix details."
