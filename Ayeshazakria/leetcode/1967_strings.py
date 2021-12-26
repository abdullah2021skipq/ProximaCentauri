
# class Solution():
#     def numOfStrings(self, patterns: List[str], word: str) -> int:
#         answer = 0
#         for substr in patterns:
#             if substr in word:
#                 answer += 1
#          return answer

class Solution(object):
    def numOfStrings(self, patterns, word):
        """
        :type patterns: List[str]
        :type word: str
        :rtype: int
        """
        res = 0
        for i in patterns:
            if i in word:
                res = res + 1
        return res