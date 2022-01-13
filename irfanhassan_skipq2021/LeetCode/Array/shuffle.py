#Given the array nums consisting of 2n elements in the form [x1,x2,...,xn,y1,y2,...,yn].

#Return the array in the form [x1,y1,x2,y2,...,xn,yn].
class Solution(object):
    def shuffle(self, nums, n):
        new_list1 = nums[0:n]
        new_list2 = nums[n:2*n]
        result = []
        for i in range(n):
            result.append(new_list1[i])
            result.append(new_list2[i])
        return result
        
test=Solution()
x=[1,2,3,4,5,6,7]
print(test.shuffle(x,3))