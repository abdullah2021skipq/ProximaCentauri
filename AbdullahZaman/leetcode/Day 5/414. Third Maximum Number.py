class Solution:
    def thirdMax(self, nums: List[int]) -> int:
        nums = set(nums)
        nums = list(nums)
        nums.sort()
        if nums[0] < nums[-1]:
            nums.reverse()
        if len(nums) >= 3:
            return nums[2]
        else:
            return nums[0]