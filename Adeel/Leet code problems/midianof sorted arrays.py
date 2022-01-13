class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
            array = nums1 + nums2
            a=len(array)
            half = int(a/2)
            array.sort()
            if a% 2 == 0:
                return (array[half - 1] + array[half] )/2 
            else:
                return array[half]