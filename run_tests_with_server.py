#!/usr/bin/env python3
"""Run all tests with automatic server management"""

import subprocess
import sys
import os
import time
import signal
import requests

server_process = None

def start_server():
    """Start the Flask server"""
    global server_process
    # Kill any existing server
    try:
        result = subprocess.run(['lsof', '-ti:5000'], capture_output=True, text=True)
        if result.returncode == 0:
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                if pid:
                    try:
                        os.kill(int(pid), signal.SIGTERM)
                    except:
                        pass
            time.sleep(1)
    except:
        pass
    
    # Start new server
    env = os.environ.copy()
    env['FLASK_APP'] = 'app.py'
    env['FLASK_ENV'] = 'development'
    
    server_process = subprocess.Popen(
        ['python3', '-m', 'flask', 'run', '--debug'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env
    )
    
    # Wait for server to start
    for i in range(30):
        try:
            response = requests.get('http://127.0.0.1:5000/clear', timeout=1)
            if response.status_code == 200:
                print("✅ Server started successfully")
                return True
        except:
            time.sleep(0.5)
    
    print("❌ Server failed to start")
    return False

def stop_server():
    """Stop the Flask server"""
    global server_process
    if server_process:
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()
        server_process = None

def run_tests():
    """Run all test cases"""
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
                timeout=30
            )
            
            output = result.stdout.strip()
            if 'Test Passed' in output:
                print(f"✅ {test_file}: PASSED")
                results[test_file] = True
            else:
                print(f"❌ {test_file}: FAILED")
                # Print first few lines of output
                lines = output.split('\n')[:3]
                for line in lines:
                    if line.strip():
                        print(f"   {line}")
                results[test_file] = False
        except subprocess.TimeoutExpired:
            print(f"⏱️  {test_file}: TIMEOUT")
            results[test_file] = False
        except Exception as e:
            print(f"❌ {test_file}: ERROR - {e}")
            results[test_file] = False
    
    return results

def main():
    """Main function"""
    try:
        if not start_server():
            sys.exit(1)
        
        time.sleep(1)  # Give server a moment to fully initialize
        
        results = run_tests()
        
        print()
        print("=" * 60)
        print("Summary")
        print("=" * 60)
        passed = sum(1 for v in results.values() if v)
        total = len(results)
        print(f"Passed: {passed}/{total}")
        
        for test_file, result in results.items():
            status = "✅" if result else "❌"
            print(f"  {status} {test_file}")
        
        print()
        
        if passed == total:
            print("🎉 All tests passed!")
            return 0
        else:
            print("⚠️  Some tests failed")
            return 1
    finally:
        stop_server()

if __name__ == '__main__':
    sys.exit(main())

