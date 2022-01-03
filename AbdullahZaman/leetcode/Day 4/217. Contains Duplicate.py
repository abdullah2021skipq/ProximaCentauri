class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        dic = {}
        counter = 1
        for i in nums:
            if i in dic:
                dic[i] += counter
            else:
                dic[i] = counter
        if dic[max(dic,key=dic.get)] > 1:
            return True
        else:
            return False