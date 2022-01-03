#Given an array of integers nums, return the number of good pairs.
#A pair (i, j) is called good if nums[i] == nums[j] and i < j.
class Solution:
    def goodpair_ofnumber(self, nums):
        count, nums_dict = 0, {}
            
        for i in range(-1, -(len(nums) + 1), -1):
            if nums[i] not in nums_dict:
                nums_dict[nums[i]] = 1
            else:
                count += nums_dict[nums[i]]
                nums_dict[nums[i]] += 1
        #print(nums_dict)
        return count
        
x=[1,2,3,1,1,3]
test=Solution()
print(test.goodpair_ofnumber(x))