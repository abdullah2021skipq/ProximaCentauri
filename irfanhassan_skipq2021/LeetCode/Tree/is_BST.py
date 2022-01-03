def checkRange(node: TreeNode, lo: int, hi:int) -> bool:
    if not node:
        return True
    elif lo is not None and node.val <= lo:
        return False
    elif hi is not None and node.val >= hi:
        return False
    return checkRange(node.left, lo, node.val) and checkRange(node.right, node.val, hi)
    
def isValidBST(root: TreeNode) -> bool:
	return checkRange(root, None, None)