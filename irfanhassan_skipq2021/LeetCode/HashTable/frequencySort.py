#Given a string s, sort it in decreasing order based on the frequency of the characters.
class Solution:
    def frequencySort(self, s):
        char_count = {}
        maxHeap = []
        result = ''
        # O(N), O(N) N = chars in s
        for char in s:
            if char not in char_count.keys():
                char_count[char] = 0
            char_count[char] += 1

        # O(D * log(D)), O(D) D = distinct chars in s
        for char, count in char_count.items():
            heappush(maxHeap, (-count, char))

        # O(D), O(1)
        while maxHeap:
            element = heappop(maxHeap)
            result += -element[0] * element[1]

        return result

s = "tree"
t=Solution()
print(t.frequencySort(s))