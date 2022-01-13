class Solution(object):
    def arrangeCoins(self, n):
        start = 0
        end = n
         
        while start + 1 < end:
            mid = start + (end - start) // 2
            
            
            if mid * (mid + 1) // 2 <= n:
                start = mid
            else:
                end = mid
                
        if end * (end + 1) // 2 <= n:
            return end
            
        return start
        """
        :type n: int
        :rtype: int
        """
        