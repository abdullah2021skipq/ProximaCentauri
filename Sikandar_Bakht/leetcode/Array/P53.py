#subarray with greatest sum

def max_subarray(nums):
    curr_max = total_max = nums[0]
    for i in range(1, len(nums)):
        curr_max = max(nums[i], curr_max + nums[i])
        total_max = max(curr_max, total_max)
    return total_max 