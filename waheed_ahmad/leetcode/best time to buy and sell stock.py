class Solution(object):
    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        l ,r = 0,0
        maxprofit= 0

        while r < len(prices):
            if prices[l] < prices [r]:
                profit = prices[r] - prices[l]
                maxprofit = max(maxprofit, profit)
            else:
                l=r
            r+=1
        return maxprofit
        
