class Solution(object):
    def missingNumber(self, nums):
        nums.sort()
        if nums[0] != 0:
            return 0
        if nums[-1] != len(nums):
            return len(nums)
        
        for i in range(1, len(nums)):
            exp_val = nums[i-1] + 1
            if nums[i] != exp_val:
                return exp_val
        """
        :type nums: List[int]
        :rtype: int
        """
        