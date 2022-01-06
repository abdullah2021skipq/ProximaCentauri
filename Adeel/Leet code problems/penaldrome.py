class Solution:
    def isPalindrome(self, x: int) -> bool:
        temp = x
        rev = 0
        if x < 0:
            return(False)
        else:
            while x > 0:
                LSB = x % 10
                rev = rev * 10 + LSB
                x = int(x/10)
        if rev == temp:
            return(True)
        else:
            return(False)