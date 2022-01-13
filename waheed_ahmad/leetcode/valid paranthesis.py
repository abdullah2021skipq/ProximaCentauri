class Solution(object):
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """
        stack = []
        ctoopen= {")" :"(", "}": "{" , "]": "[" }
        for c in s:
            if c in ctoopen:
                if stack and stack[-1]== ctoopen[c]:
                    stack.pop()
                else:
                    return False
            else:
                stack.append(c)
        return True if not stack else False
        
