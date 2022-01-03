class Solution(object):
    def majorityElement(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        result = 0
        count = 0
        for n in nums :
            if count==0:
                result = n
            if n== result:
                count +=1
            else:
                count-=1
        return result
