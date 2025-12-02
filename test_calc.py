
def smooth_profile(erls, prls, max_lift, max_lower, iterations=50):
    n = len(prls)
    if n < 3: return prls
    
    new_prls = prls[:]
    
    for _ in range(iterations):
        temp_prls = new_prls[:]
        for i in range(1, n-1):
            # 1. Smoothing
            smoothed = (temp_prls[i-1] + temp_prls[i+1]) / 2.0
            
            # 2. Constraints
            upper_limit = erls[i] + max_lift
            lower_limit = erls[i] - max_lower
            
            if smoothed > upper_limit:
                smoothed = upper_limit
            elif smoothed < lower_limit:
                smoothed = lower_limit
                
            new_prls[i] = smoothed
            
    return new_prls

# Test Case 1: Simple Dip
erls = [100.0, 99.0, 100.0]
prls = [100.0, 99.0, 100.0] # Initial PRL = ERL
max_lift = 0.5
max_lower = 0.0

# Expected: Middle point should try to go to 100, but capped at 99.5
result = smooth_profile(erls, prls, max_lift, max_lower)
print(f"Test 1 (Dip with Limit): {result}")
assert abs(result[1] - 99.5) < 0.001

# Test Case 2: No Limit
max_lift = 10.0
result = smooth_profile(erls, prls, max_lift, max_lower)
print(f"Test 2 (Dip No Limit): {result}")
assert abs(result[1] - 100.0) < 0.001

print("All tests passed!")
