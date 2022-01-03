#A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.
class Solution:
    def isPalindrome(self, string):
        string = string.lower()
        string = ''.join(ch for ch in string if ch.isalnum())
        j = string[::-1]
        if string == j:
            return True
        else:
            return False
test=Solution()
string = "A man, a plan, a canal: Panama"
print(test.isPalindrome(string))