class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        a = 0
        for items in nums:
            b = 0
            cmd = False
            for num in nums:
                if items + num == target and a < b:
                    cmd = True
                    break
                b += 1
            if cmd:
                break
            a += 1
        return [a,b]