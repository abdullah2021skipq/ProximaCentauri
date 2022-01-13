class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        ans = [-1,-1]
        l,r = 0,len(nums)
        
        #For first value
        while l < r:
            mid = (l+r)//2
            if nums[mid] == target:
                if mid == 0:
                    ans[0] = 0
                    break
                elif mid - 1 >= 0 and nums[mid-1] != target:
                    ans[0] = mid
                    break
                else:
                    r = mid
            elif nums[mid] < target:
                l = mid + 1
            else:
                r = mid
        l,r = 0, len(nums)
        
        #For last value
        while l < r:
            mid = (l+r)//2
            if nums[mid] == target:
                if mid + 1 == len(nums):
                    ans[1] = len(nums) - 1
                    break
                elif mid + 1 < len(nums) and nums[mid+1] != target:
                    ans[1] = mid
                    break
                else:
                    l = mid
            elif nums[mid] < target:
                l = mid + 1
            else:
                r = mid
        
                
        return ans