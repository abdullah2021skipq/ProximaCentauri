#combination sum
def combinationSum(candidates, target):

    candidates.sort()
    ans = []
    def helper(candidates, target, t):
        if not target:
            ans.append(t)
            return
        for i, num in enumerate(candidates):
            if target >= num:
                helper(candidates[i:], target - num, t + [num])
            else: break
    helper(candidates, target, [])
    return ans