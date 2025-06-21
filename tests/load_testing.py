#!/usr/bin/env python3
"""
Load testing script to validate scaling
Run this from your local machine with port-forward active
"""

import requests
import time
import threading
from collections import defaultdict
import statistics

# Configuration
BACKEND_URL = "http://localhost:5000/api"
FRONTEND_URL = "http://localhost:8080"
NUM_REQUESTS = 200
CONCURRENT_THREADS = 20

def test_backend():
    """Test backend API endpoint"""
    response_times = []
    success_count = 0
    
    for i in range(NUM_REQUESTS // CONCURRENT_THREADS):
        start_time = time.time()
        try:
            response = requests.get(BACKEND_URL, timeout=5)
            end_time = time.time()
            
            if response.status_code == 200:
                success_count += 1
                response_times.append(end_time - start_time)
                print(f"Backend request {i+1}: {response.json()['message'][:30]}... ({end_time - start_time:.3f}s)")
                print(f"podname {i}: {response.json()['pod_name']}... ({end_time - start_time:.3f}s)")
            else:
                print(f"Backend request {i+1}: ERROR {response.status_code}")
                
        except Exception as e:
            print(f"Backend request {i+1}: FAILED - {str(e)}")
        
        time.sleep(0.1)  # Small delay between requests
    
    return response_times, success_count

def test_frontend():
    """Test frontend endpoint"""
    response_times = []
    success_count = 0
    
    for i in range(NUM_REQUESTS // CONCURRENT_THREADS):
        start_time = time.time()
        try:
            response = requests.get(FRONTEND_URL, timeout=5)
            end_time = time.time()
            
            if response.status_code == 200:
                success_count += 1
                response_times.append(end_time - start_time)
                print(f"Frontend request {i+1}: OK ({end_time - start_time:.3f}s)")
            else:
                print(f"Frontend request {i+1}: ERROR {response.status_code}")
                
        except Exception as e:
            print(f"Frontend request {i+1}: FAILED - {str(e)}")
        
        time.sleep(0.1)
    
    return response_times, success_count

def main():
    print("=== Starting Load Test ===")
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Frontend URL: {FRONTEND_URL}")
    print(f"Total requests: {NUM_REQUESTS}")
    print(f"Concurrent threads: {CONCURRENT_THREADS}")
    print()
    
    # Start concurrent tests
    threads = []
    results = {"backend": [], "frontend": []}
    
    # Backend threads
    for i in range(CONCURRENT_THREADS):
        thread = threading.Thread(target=lambda: results["backend"].append(test_backend()))
        threads.append(thread)
        thread.start()
    
    # Frontend threads  
    for i in range(CONCURRENT_THREADS):
        thread = threading.Thread(target=lambda: results["frontend"].append(test_frontend()))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads
    for thread in threads:
        thread.join()
    
    # Analyze results
    print("\n=== Results ===")
    
    for service in ["backend", "frontend"]:
        all_times = []
        total_success = 0
        
        for times, success in results[service]:
            all_times.extend(times)
            total_success += success
        
        if all_times:
            print(f"\n{service.upper()} Results:")
            print(f"  Total successful requests: {total_success}")
            print(f"  Success rate: {total_success/NUM_REQUESTS*100:.1f}%")
            print(f"  Average response time: {statistics.mean(all_times):.3f}s")
            print(f"  Min response time: {min(all_times):.3f}s")
            print(f"  Max response time: {max(all_times):.3f}s")
            if len(all_times) > 1:
                print(f"  Standard deviation: {statistics.stdev(all_times):.3f}s")

if __name__ == "__main__":
    main()