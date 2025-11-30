#!/bin/bash

# Test script to verify critical fixes before deployment

echo "🧪 Testing Critical Fixes..."
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Check Python imports
echo "1️⃣  Testing Python imports..."
cd backend

python3 << 'EOF'
import sys
sys.path.insert(0, '..')

try:
    # Test storage import
    from backend import storage
    print("✓ storage import successful")
    
    # Test usage import
    from backend import usage
    print("✓ usage import successful")
    
    # Test database import
    from backend import database
    print("✓ database import successful")
    
    # Test models import
    from backend import models
    print("✓ models import successful")
    
    # Test council import
    from backend import council
    print("✓ council import successful")
    
    print("\n✅ All imports working correctly!")
    sys.exit(0)
    
except Exception as e:
    print(f"\n❌ Import error: {e}")
    sys.exit(1)
EOF

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Python imports test passed${NC}"
else
    echo -e "${RED}✗ Python imports test failed${NC}"
    exit 1
fi

cd ..
echo ""

# Test 2: Check frontend build
echo "2️⃣  Testing frontend build..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

echo "Building frontend..."
npm run build

if [ -d "dist" ] && [ -f "dist/index.html" ]; then
    echo -e "${GREEN}✓ Frontend build successful${NC}"
    echo "  - dist/ directory exists"
    echo "  - index.html found"
    
    # Check for assets
    if [ -d "dist/assets" ]; then
        echo "  - assets/ directory found"
    fi
else
    echo -e "${RED}✗ Frontend build failed${NC}"
    exit 1
fi

cd ..
echo ""

# Test 3: Check environment variables
echo "3️⃣  Checking environment variables..."

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
        echo -e "  ${YELLOW}⚠ DATABASE_URL missing (will use JSON storage)${NC}"
    fi
else
    echo -e "${YELLOW}⚠ .env file not found${NC}"
fi

echo ""

# Test 4: Check file structure
echo "4️⃣  Checking file structure..."

files_to_check=(
    "backend/main.py"
    "backend/storage.py"
    "backend/usage.py"
    "backend/database.py"
    "backend/storage_postgres.py"
    "backend/usage_postgres.py"
    "backend/models.py"
    "backend/council.py"
    "frontend/dist/index.html"
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

# Test 5: Check for proper imports in key files
echo "5️⃣  Checking import statements..."

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

if [ "$all_imports_correct" = true ]; then
    echo -e "${GREEN}✓ All imports are correct${NC}"
else
    echo -e "${RED}✗ Some imports need fixing${NC}"
    exit 1
fi

echo ""

# Test 6: Check for frontend serving in main.py
echo "6️⃣  Checking frontend serving configuration..."

if grep -q "StaticFiles" "backend/main.py"; then
    echo "  ✓ StaticFiles import found"
else
    echo -e "  ${RED}✗ StaticFiles import missing${NC}"
    exit 1
fi

if grep -q "app.mount.*assets.*StaticFiles" "backend/main.py"; then
    echo "  ✓ Assets mounting configured"
else
    echo -e "  ${RED}✗ Assets mounting not configured${NC}"
    exit 1
fi

if grep -q "full_path:path" "backend/main.py"; then
    echo "  ✓ Catch-all route for SPA found"
else
    echo -e "  ${RED}✗ Catch-all route missing${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Frontend serving configured correctly${NC}"
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ All tests passed!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Next steps:"
echo "1. Commit changes: git add . && git commit -m 'Fix: Critical issues'"
echo "2. Push to Railway: git push"
echo "3. Monitor deployment logs"
echo "4. Test the deployed application"
echo ""
echo "See DEPLOYMENT_GUIDE.md for detailed deployment instructions."
