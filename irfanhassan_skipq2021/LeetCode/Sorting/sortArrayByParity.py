#Given an integer array nums, move all the even integers at the beginning of the array followed by all the odd integers.

#Return any array that satisfies this condition.
class Solution:
    def sortArrayByParity(self, nums):
        left, right = 0, len(nums) - 1
        
        while left <= right:
            if nums[right] % 2 == 0:
                nums[left], nums[right] = nums[right], nums[left]
                left += 1
            else:
                right -= 1
        
        return nums

x=[1,3,5,4]
test=Solution()
print(test.sortArrayByParity(x))