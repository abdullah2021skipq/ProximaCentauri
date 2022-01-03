#Given the root node of a binary search tree and two integers low and high, return the sum of values of all nodes with a value in the inclusive range [low, high].

class Solution:
    def rangeSumBST(self, root, low, high):
        r = range(low, high+1)
        
        def recurse(root):
            if root == None:
                return 0
            if root.val in r:
                return recurse(root.left) + recurse(root.right) + root.val
            else:  
                return recurse(root.left) + recurse(root.right)
            
        return recurse(root)