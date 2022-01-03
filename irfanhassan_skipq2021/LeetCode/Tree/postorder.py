#Given the root of an n-ary tree, return the postorder traversal of its nodes' values.
class Solution(object):
	def postorder(self, root):
		res=[]
		def bfs(root):
			if root:
				for child in root.children:
					bfs(child)
				res.append(root.val)
		bfs(root)

		return res