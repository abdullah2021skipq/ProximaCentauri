class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        a = 0
        i = len(nums1)-1
        if len(nums1)==1:
           if nums1[a] ==0:
               nums1[a] = nums2[a]
        else:
            while i>=0:
                if nums1[i] == 0:
                    nums1[i]=nums2[a] 
                    a+=1
                    i-=1
                if m-1==i:
                    break
            nums1.sort()