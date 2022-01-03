class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        pro = 0
        if len(prices)==1:
            return 0
        else:
            for i in range(len(prices)-1):
                if prices[i]<prices[i+1]:
                        pro = pro + (prices[i+1] - prices[i])
                    
            return pro
                       