class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        dic = {}
        counter = 1
        for i in nums:
            if i in dic:
                dic[i] += counter
            else:
                dic[i] = counter
        return max(dic, key=dic.get)