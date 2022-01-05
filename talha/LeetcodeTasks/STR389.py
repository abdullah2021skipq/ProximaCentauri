class Solution(object):
    def findTheDifference(self, s, t):
        s_list = list(s)
        t_list = list(t)
        for i in s_list:
            t_list.remove(i)
        return t_list[0]
        """
        :type s: str
        :type t: str
        :rtype: str
        """
        