class Solution:
    #this function rorate array to right by n times and will return update array 
    def rotate_array(self, array, n):
        length = len(array)
        n = n % length
        sp = length - n
        array[:] = array[sp:] + array[:sp]
        return array
        
test = Solution()
array=[1,2,3,4,5,6]
time =3
print(test.rotate_array(array,time))