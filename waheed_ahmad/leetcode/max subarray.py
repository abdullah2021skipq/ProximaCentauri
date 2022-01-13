class Solution(object):
    def maxSubArray(self, nums):
     
        result = nums[0]
        curr = 0
        for n in nums:
            curr = max(curr+n, n)
            result = max(result, curr)
        return result

        
