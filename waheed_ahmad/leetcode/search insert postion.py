class Solution(object):
    def searchInsert(self, nums, target):

        left = 0
        right = len(nums) - 1
        while left <= right:
            mid = left + (right - left) / 2
            if nums[mid] >= target:
                right = mid - 1
            else:
                left = mid + 1

        return left


