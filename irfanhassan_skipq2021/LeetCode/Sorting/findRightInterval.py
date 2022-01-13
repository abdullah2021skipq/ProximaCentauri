class Solution:
    def findRightInterval(self, intervals):
        starts = sorted((s, j) for j, (s, e) in enumerate(intervals))
        res = [-1] * len(intervals)
        len_starts = len(starts)
        for i, (_, e) in enumerate(intervals):
            left, right = 0, len_starts - 1
            if starts[left][0] == e:
                res[i] = starts[left][1]
                continue
            if starts[right][0] >= e:
                while right - left > 1:
                    middle = (left + right) // 2
                    if starts[middle][0] >= e:
                        right = middle
                    else:
                        left = middle
                res[i] = starts[right][1]
        return res
        
z=[1,2]
t=Solution()
print(t.findRightInterval(z))