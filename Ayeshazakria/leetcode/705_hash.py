from typing import Collection


def findShortestSubArray(self, nums):

    freq = Collection.defaultdict(int)
    
    for num in nums:
        freq[num]+=1
    max_freq = max(freq.values())
    
    
    l, minLen, cur_freq = 0, len(nums), Collection.defaultdict(int)
    for r in range(len(nums)):
        cur_freq[nums[r]]+=1
      
        if cur_freq[nums[r]] == max_freq:
            while cur_freq[nums[r]]==max_freq:
                cur_freq[nums[l]]-=1
                l +=1
            cur_freq[nums[r]]+=1
            minLen = min(minLen, r - l + 2)
            
    return minLen
