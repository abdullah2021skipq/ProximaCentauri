# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        list = []
        def reverse(node):
            if node is None:
                return
            else:
                reverse(node.left)
                list.append(node.val)
                reverse(node.right)
        reverse(root)
        return list