class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class MaxHeap:
    def __init__(self):
        self.heap = []

    def insert(self, item):
        self.heap.append(item)
        self._heapify_up(len(self.heap) - 1)

    def extract_max(self):
        if len(self.heap) > 1:
            self._swap(0, len(self.heap) - 1)
            max_item = self.heap.pop()
            self._heapify_down(0)
        elif self.heap:
            max_item = self.heap.pop()
        else:
            max_item = None
        return max_item

    def _heapify_up(self, index):
        parent = (index - 1) // 2
        if index > 0 and self.heap[parent] < self.heap[index]:
            self.heap[parent], self.heap[index] = self.heap[index], self.heap[parent]
            self._heapify_up(parent)

    def _heapify_down(self, index):
        left = 2 * index + 1
        right = 2 * index + 2
        largest = index

        if left < len(self.heap) and self.heap[left] > self.heap[largest]:
            largest = left

        if right < len(self.heap) and self.heap[right] > self.heap[largest]:
            largest = right

        if largest != index:
            self._swap(index, largest)
            self._heapify_down(largest)


class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        new_node = Node(key)
        if not self.root:
            self.root = new_node
        else:
            self.root = self._insert_avl(self.root, new_node)

    def _insert_avl(self, root, node):
        if root is None:
            return node
        if node.key < root.key:
            root.left = self._insert_avl(root.left, node)
        else:
            root.right = self._insert_avl(root.right, node)

        balance = self._calc_height_diff(root)

        if balance > 1:
            if node.key < root.left.key:
                return self._rotateLL(root)
            else:
                return self._rotateLR(root)
        elif balance < -1:
            if node.key > root.right.key:
                return self._rotateRR(root)
            else:
                return self._rotateRL(root)

        return root

    def _calc_height_diff(self, root):
        return self.height(root.left) - self.height(root.right)

    def height(self, node):
        if node is None:
            return 0
        return max(self.height(node.left), self.height(node.right)) + 1

    def _rotateLL(self, A):
        B = A.left
        A.left = B.right
        B.right = A
        return B

    def _rotateRR(self, A):
        B = A.right
        A.right = B.left
        B.left = A
        return B

    def _rotateRL(self, A):
        B = A.right
        A.right = self._rotateLL(B)
        return self._rotateRR(A)

    def _rotateLR(self, A):
        B = A.left
        A.left = self._rotateRR(B)
        return self._rotateLL(A)

    def find_min(self, root):
        while root.left is not None:
            root = root.left
        return root

    def delete(self, key):
        self.root = self._delete_node(self.root, key)

    def _delete_node(self, root, key):
        if root is None:
            return root

        if key < root.key:
            root.left = self._delete_node(root.left, key)
        elif key > root.key:
            root.right = self._delete_node(root.right, key)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left

            temp = self.find_min(root.right)
            root.key = temp.key
            root.right = self._delete_node(root.right, temp.key)

        if root is None:
            return root

        balance = self._calc_height_diff(root)

        if balance > 1:
            if self._calc_height_diff(root.left) >= 0:
                return self._rotateLL(root)
            else:
                return self._rotateLR(root)
        if balance < -1:
            if self._calc_height_diff(root.right) <= 0:
                return self._rotateRR(root)
            else:
                return self._rotateRL(root)

        return root

    def search(self, key):
        return self._search_node(self.root, key)

    def _search_node(self, root, key):
        if root is None or root.key == key:
            return root

        if key < root.key:
            return self._search_node(root.left, key)
        return self._search_node(root.right, key)
    # 중위 순회

    def in_order_traversal(self, root, result=[]):
        if root is not None:
            self.in_order_traversal(root.left, result)
            result.append(root.key)
            self.in_order_traversal(root.right, result)
        return result
