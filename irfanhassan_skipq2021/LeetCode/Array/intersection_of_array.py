''''
Given two integer arrays nums1 and nums2, return an array of their intersection. Each element in the result must appear as many times as it shows in both arrays and you may return the result in any order.
'''

class Solution:
    def intersect_of_arrays(self, arr1, arr2):
        length1 = len(arr1)
        length2 = len(arr2)
        result = []
        for value in arr1:
            if value in arr2:
                result.append(value)
        return result
        
TEST=Solution()
arr1=[1,2,3,4,5]
arr2=[1,3,5]
print(TEST.intersect_of_arrays(arr1,arr2))