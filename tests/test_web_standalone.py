# tests/test_trending_standalone.py
import sys
import os

# Add the parent directory to the path so we can import your tools
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Assuming you saved the function in market_tools.py
from market_tools import get_trending_crops 

def run_trending_test():
    print("🚀 Starting Standalone Trending Crops Test...\n")
    
    # Test 1: A massive market hub (Should have plenty of data)
    district_1 = "PUNE"
    print(f"🔍 Fetching trends for: {district_1}")
    result_1 = get_trending_crops(district_1)
    print(result_1)
    print("="*60 + "\n")

    # Test 2: Another district we saw in your HTML dump earlier
    district_2 = "JALGAON"
    print(f"🔍 Fetching trends for: {district_2}")
    result_2 = get_trending_crops(district_2)
    print(result_2)
    print("="*60 + "\n")
    
    # Test 3: Error handling test (A district that doesn't exist)
    district_3 = "FAKE_CITY"
    print(f"🔍 Fetching trends for: {district_3}")
    result_3 = get_trending_crops(district_3)
    print(result_3)

if __name__ == "__main__":
    run_trending_test()