# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def rangeSumBST(self, root: Optional[TreeNode], low: int, high: int) -> int:
        list = []
        def reverse(node):
            if node is None:
                return
            else:
                reverse(node.left)
                if node.val >= low and node.val<= high:
                    list.append(node.val)
                reverse(node.right)
        reverse(root)
        ans = sum(list)
        return ans