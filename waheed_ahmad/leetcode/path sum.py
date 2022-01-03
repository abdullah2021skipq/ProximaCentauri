# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def hasPathSum(self, root, targetSum):
        """
        :type root: TreeNode
        :type targetSum: int
        :rtype: bool
        """
        def dfs(node, sum):
            if not node:
                return False
            sum += node.val
            if not node.left and not node.right:
                if (sum == targetSum):
                    return True
                else:
                    return False

            return (dfs(node.left, sum) or dfs(node.right , sum))
        return dfs(root,0)
