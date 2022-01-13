#Return a list of the target indices of nums after sorting nums in non-decreasing order. If there are no target indices, return an empty list.
class Solution:
    def targetIndices(self, nums, target):
        ans = []
        sortednums = sorted(nums)
        for i in range(len(sortednums)):
            if sortednums[i] == target:
                ans.append(i)
                
        return ans
        
test=Solution()
x=[1,2,3,4,5,3,1]
target=3
print(test.targetIndices(x,target))