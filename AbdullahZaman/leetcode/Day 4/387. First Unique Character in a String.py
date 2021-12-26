class Solution:
    def firstUniqChar(self, s: str) -> int:
        dic = {}
        constant = 1
        for i in s:
            if i in dic:
                dic[i] += 1
            else:
                dic[i] = 1
        for key, value in dic.items():
            if value == 1:
                return s.index(key)
        return -1