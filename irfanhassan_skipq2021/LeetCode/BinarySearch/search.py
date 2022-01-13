#Given an array of integers nums which is sorted in ascending order, and an integer target, write a function to search target in nums. If target exists, then return its index. Otherwise, return -1.
class Solution:
    def search(self, nums, target):
        L,R = 0, len(nums)-1
        while L<=R:
            mid = (L+R)//2
            if nums[mid]==target:
                return mid
            elif nums[mid]>target:
                R = mid -1
            elif nums[mid]<target: 
                L = mid + 1
        return -1
        
x=[1,2,3,4,5,6,7]
test=Solution()
print(test.search(x,4))