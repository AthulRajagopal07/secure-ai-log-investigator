#!/usr/bin/env bash

set -e

echo "=============================================="
echo "       SECURE AI LOG INVESTIGATOR"
echo "=============================================="

echo ""
echo "Step 1: Generate synthetic production logs"
python generate_logs.py

echo ""
echo "Step 2: Show raw log volume"
wc -l logs/raw_app.log

echo ""
echo "Step 3: Show raw logs"
head -3 logs/raw_app.log

echo ""
echo "Step 4: Sanitize logs"
python sanitizer.py

echo ""
echo "Step 5: Compare raw vs sanitized logs"

echo "RAW:"
head -2 logs/raw_app.log

echo ""
echo "SANITIZED:"
head -2 logs/sanitized_app.log

echo ""
echo "Step 6: Run security gate"
python security_scanner.py

echo ""
echo "Step 7: Extract incident patterns"
python pattern_extractor.py

echo ""
echo "Step 8: Estimate token reduction"
python token_estimator.py

echo ""
echo "Step 9: Run local AI investigation"
python ai_investigator.py

echo ""
echo "=============================================="
echo "Investigation completed successfully."
echo "=============================================="