#Input: s = "3[a]2[bc]"
#Output: "aaabcbc"
#look exmaple of decoding
class Solution:
    def decodeString(self, s: str) -> str:
        stack, num = [], 0
        for c in s:
            if '0' <= c <= '9':
                num = 10 * num + ord(c) - ord('0')
            elif c == '[':
                stack.append(num)
                num = 0
            elif c == ']':
                t = ''
                while not isinstance(stack[-1], int):
                    t = stack.pop() + t
                stack.append(stack.pop() * t)
            else:
                stack.append(c)
            
        return ''.join(stack)
        
t=Solution()
Input= "2[ad]2[bc]"
print(t.decodeString(Input))