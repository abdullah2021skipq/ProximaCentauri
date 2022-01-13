class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        a = nums
        b = 0
        for i in range(len(nums)):
            if nums[i] == val:
                continue
            else:
                a[b] = nums[i] 
                b+=1
        nums = a
        return b