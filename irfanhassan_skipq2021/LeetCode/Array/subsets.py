#Given an integer array nums of unique elements, return all possible subsets (the power set).
class Solution:
    def subsets(self, nums):
        ans = [[]]
        for num in nums:
            for i in range(len(ans)):
                ans.append([*ans[i], num])
        return ans

t=Solution()        
nums = [1,2]
print(t.subsets(nums))