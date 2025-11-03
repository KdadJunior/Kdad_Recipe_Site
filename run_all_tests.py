#!/usr/bin/env python3
"""Run all test cases and report results"""

import subprocess
import sys
import os

test_files = [
    'test-regression-create-user-checkpoint.py',
    'test-regression-login-checkpoint.py',
    'test-create-recipe-checkpoint.py',
    'test-like-recipe-checkpoint.py',
    'test-view-recipe-attributes.py',
    'test-search-recipe.py',
    'test-delete-user.py'
]

base_dir = 'project-2-released-cases'
results = {}

print("=" * 60)
print("Running All Test Cases")
print("=" * 60)
print()

for test_file in test_files:
    test_path = os.path.join(base_dir, test_file)
    if not os.path.exists(test_path):
        print(f"❌ {test_file}: File not found")
        results[test_file] = False
        continue
    
    try:
        result = subprocess.run(
            ['python3', test_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        output = result.stdout.strip()
        if 'Test Passed' in output:
            print(f"✅ {test_file}: PASSED")
            results[test_file] = True
        else:
            print(f"❌ {test_file}: FAILED")
            print(f"   Output: {output}")
            if result.stderr:
                print(f"   Error: {result.stderr}")
            results[test_file] = False
    except subprocess.TimeoutExpired:
        print(f"⏱️  {test_file}: TIMEOUT")
        results[test_file] = False
    except Exception as e:
        print(f"❌ {test_file}: ERROR - {e}")
        results[test_file] = False

print()
print("=" * 60)
print("Summary")
print("=" * 60)
passed = sum(1 for v in results.values() if v)
total = len(results)
print(f"Passed: {passed}/{total}")
print()

if passed == total:
    print("🎉 All tests passed!")
    sys.exit(0)
else:
    print("⚠️  Some tests failed")
    sys.exit(1)

