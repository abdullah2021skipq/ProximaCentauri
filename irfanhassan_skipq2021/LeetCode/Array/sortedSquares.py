#Given an integer array nums sorted in non-decreasing order, return an array of the squares of each number sorted in non-decreasing order.
class Solution:
    def sortedSquares(self, nums):
        nums_sq = [i**2 for i in nums]
        nums_sq.sort()
        return nums_sq
test=Solution()      
x=[1,3,2,5]
print(test.sortedSquares(x))
