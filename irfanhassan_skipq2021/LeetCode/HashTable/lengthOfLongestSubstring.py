#finding length of substring having unique characters
class Solution:
	def lengthOfLongestSubstring(self, s):
		res = 0
		ls = ""   #longest substring
		for c in s:
			if c in ls:
				res = max(res,len(ls))
				ls = ls[ls.find(c)+1:] + c
			else:
				ls += c
		res = max(res,len(ls))
		return res
test=Solution()
x=input(":")
print(test.lengthOfLongestSubstring(x))