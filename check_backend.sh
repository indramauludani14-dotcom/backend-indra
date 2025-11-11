#!/bin/bash
# Script untuk test struktur backend di cPanel

echo "======================================"
echo "BACKEND STRUCTURE CHECK"
echo "======================================"

cd /home/virtuali/api || exit 1

echo -e "\n[1] Files in /api:"
ls -lh | grep -E "\.py$|\.txt$|htaccess"

echo -e "\n[2] Folders:"
ls -ld */ 2>/dev/null

echo -e "\n[3] routes/api.py exists:"
if [ -f "routes/api.py" ]; then
    echo "✓ YES"
    wc -l routes/api.py
else
    echo "✗ NO - FILE MISSING!"
fi

echo -e "\n[4] Blueprint registration in app.py:"
if grep -q "register_blueprint" app.py; then
    echo "✓ Found:"
    grep -n "register_blueprint" app.py
else
    echo "✗ NOT FOUND - Blueprint not registered!"
fi

echo -e "\n[5] Routes defined in routes/api.py:"
grep -n "^@api.route\|^@app.route" routes/api.py 2>/dev/null | head -10

echo -e "\n[6] Test import:"
python3 -c "import sys; sys.path.insert(0, '.'); from app import app; print('✓ app.py imports successfully')" 2>&1

echo -e "\n[7] Flask routes:"
python3 -c "from app import app; print('\n'.join([str(rule) for rule in app.url_map.iter_rules()]))" 2>&1 | head -15

echo -e "\n======================================"
echo "Check complete!"
