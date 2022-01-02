#running sum of 1d array
def runningSum(nums):
    sum= [nums[0]]
    for i in range(1, len(nums)):
        sum.append(sum[i-1] + nums[i])
        
    return sum
    
num = [1, 2, 3, 4]
print(runningSum(num))