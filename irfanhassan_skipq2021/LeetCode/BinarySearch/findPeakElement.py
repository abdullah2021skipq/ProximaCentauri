class Solution:
    def findPeakElement(self, nums):
        toright = [1] * len(nums) + [-1]
        lval = float('-inf')
        for i in range(len(nums)):
            if nums[i] > lval:
                lval = nums[i]
                continue
            elif nums[i] == lval:
                toright[i] = 0
            else:
                toright[i] = -1
            lval = nums[i]
        for idx in range(len(toright) - 1):
            if toright[idx] == 1 and toright[idx + 1] == -1:
                return idx
        return -1
        
t=Solution()
nums = [1,2,3,1]
print(t.findPeakElement(nums))