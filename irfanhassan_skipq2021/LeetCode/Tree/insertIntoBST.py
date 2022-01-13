def insertIntoBST(self, root, val):
        if root is None:
            return TreeNode(val)       
        if root.right is None and root.val < val:
            root.right = TreeNode(val)
        elif root.left is None and val < root.val:
            root.left = TreeNode(val)
        if root.val > val:
            self.insertIntoBST(root.left, val)
        else:
            self.insertIntoBST(root.right, val)
        return root