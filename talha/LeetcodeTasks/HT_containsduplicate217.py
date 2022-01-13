class Solution(object):
    def containsDuplicate(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """
        counter = set()
        
        for num in nums:
            if num not in counter:
                counter.add(num)
            else:
                return True
            
        return False