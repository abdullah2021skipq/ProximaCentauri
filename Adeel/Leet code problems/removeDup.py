class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        l = len(nums)
        del_c = 0
        for i in range(1, len(nums)):
          d = i - del_c
          if nums[d - 1] == nums[d]:
            del nums[d]
            l -= 1
            del_c += 1
        return l