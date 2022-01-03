class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        def square(n):
            return n**2
        nums = map(square,nums)
        return sorted(list(nums))