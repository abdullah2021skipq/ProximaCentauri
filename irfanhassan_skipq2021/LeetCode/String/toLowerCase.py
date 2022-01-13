#Given a string s, return the string after replacing every uppercase letter with the same lowercase letter.
class Solution:
    def toLowerCase(self, s: str) -> str:
        res = ""
        
        for i in s:
            if ord(i) >= 65 and ord(i) <= 90:
                res += chr(ord(i) + 32)
            else:
                res += i
                
        return res
        
name="IRFAN"
test=Solution()
print(test.toLowerCase(name))    