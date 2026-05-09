# 树与二叉树

## 定义
树是一种非线性结构，由结点和边构成，具有层次关系。
二叉树是每个结点最多只有两个孩子的树结构，两个孩子分别称为左孩子和右孩子。

树形结构就像是一棵真实的树：
- **根节点**：树的根部，唯一没有父节点的节点
- **子节点**：从某个节点分支出去的节点
- **叶节点**：没有子节点的节点，像树叶
- **路径**：从一个节点到另一个节点的路线
- **深度**：从根节点到该节点的路径长度
- **高度**：从该节点到最远叶节点的路径长度

生活比喻：
- 家族树：祖父母→父母→子女→孙子女
- 组织架构：CEO→总监→经理→员工
- 文件系统：根目录→子目录→文件
- 图书分类：总类→子类→具体书籍

## 原理
树适合描述具有层次关系的数据。
二叉树常见遍历包括前序、中序、后序和层序。
完全二叉树适合顺序存储，二叉链表适合链式存储。

### 基本术语
- **节点（Node）**：树中的每一个元素，包含存储的数据和指向其子节点的链接
- **根节点（Root）**：位于树顶端的节点，是整棵树的起点，一棵树有且仅有一个根节点
- **父节点与子节点（Parent & Child）**：如果一个节点 A 连接到下方的节点 B，那么 A 是 B 的父节点，B 是 A 的子节点
- **兄弟节点（Siblings）**：拥有同一个父节点的节点们互为兄弟节点
- **叶子节点（Leaf）**：没有子节点的节点，也称为终端节点
- **边（Edge）**：连接两个节点的线，表示它们之间的关系
- **路径（Path）**：从根节点到某个特定节点所经过的节点序列
- **高度（Height）**：从某个节点到其最远叶子节点的最长路径上的边数，树的高度即根节点的高度
- **深度（Depth）**：从根节点到某个节点的路径上的边数，根节点的深度为 0
- **层（Level）**：深度相同的所有节点属于同一层，根节点在第 0 层

### 树的基本性质
1. **唯一路径**：树中任意两个节点之间有且仅有一条路径
2. **N 个节点，N-1 条边**：一棵具有 N 个节点的树，总共有 N-1 条边
3. **无环**：树中不存在环（即从某个节点出发，沿着边最终又能回到该节点）

### 为什么需要树？
- **数组**：查找快（通过索引），但插入和删除慢（需要移动大量元素）
- **链表**：插入和删除快，但查找慢（需要从头遍历）
- **树（特别是二叉搜索树）**：在保持数据有序的同时，能提供比链表快得多的搜索速度，以及比数组更高效的插入/删除操作

实际应用场景：
- 文件系统：计算机中的文件夹和文件
- 数据库索引：B 树、B+ 树是数据库实现高效查询的核心
- 组织结构图：公司或部门的层级管理
- 决策树：人工智能和机器学习中的分类模型
- HTML DOM：网页文档对象模型就是一棵树

### 二叉树的遍历
遍历是指按照某种规则访问树中的每一个节点，且每个节点只访问一次。

1. **前序遍历（Pre-order）**：根 -> 左 -> 右
   - 先访问根节点，然后递归地前序遍历左子树，最后递归地前序遍历右子树
   - 应用：复制一棵树、获取前缀表达式

2. **中序遍历（In-order）**：左 -> 根 -> 右
   - 先递归地中序遍历左子树，然后访问根节点，最后递归地中序遍历右子树
   - 应用：在二叉搜索树中，中序遍历会以升序输出所有值

3. **后序遍历（Post-order）**：左 -> 右 -> 根
   - 先递归地后序遍历左子树，然后递归地后序遍历右子树，最后访问根节点
   - 应用：删除一棵树、计算目录大小

4. **层序遍历（Level-order）**：按层，从左到右
   - 从根节点开始，一层一层地访问节点
   - 应用：按层级处理数据，通常使用队列辅助实现

示例：
```
        1
       / \
      2   3
     / \   \
    4   5   6
```
- 前序：1, 2, 4, 5, 3, 6
- 中序：4, 2, 5, 1, 3, 6
- 后序：4, 5, 2, 6, 3, 1
- 层序：1, 2, 3, 4, 5, 6

## 示例
### Python 实现二叉树
```python
class TreeNode:
    """二叉树节点类"""
    def __init__(self, value):
        self.value = value  # 节点存储的数据
        self.left = None    # 指向左子节点
        self.right = None   # 指向右子节点

def preorder_traversal(node):
    """前序遍历：根 -> 左 -> 右"""
    if node is None:
        return
    print(node.value, end=' ')
    preorder_traversal(node.left)
    preorder_traversal(node.right)

def inorder_traversal(node):
    """中序遍历：左 -> 根 -> 右"""
    if node is None:
        return
    inorder_traversal(node.left)
    print(node.value, end=' ')
    inorder_traversal(node.right)

def postorder_traversal(node):
    """后序遍历：左 -> 右 -> 根"""
    if node is None:
        return
    postorder_traversal(node.left)
    postorder_traversal(node.right)
    print(node.value, end=' ')
```

### 二叉搜索树操作
```python
class BinarySearchTree:
    def __init__(self):
        self.root = None
    
    def insert(self, value):
        """插入节点"""
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self._insert_recursive(self.root, value)
    
    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert_recursive(node.right, value)
    
    def search(self, value):
        """查找节点"""
        return self._search_recursive(self.root, value)
    
    def _search_recursive(self, node, value):
        if node is None or node.value == value:
            return node
        if value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)
```

## 易错点
1. 学生容易把"满二叉树""完全二叉树""二叉排序树"混为一谈
   - **满二叉树**：每个节点都有 0 或 2 个子节点
   - **完全二叉树**：除最后一层外都是满的，最后一层节点靠左排列
   - **二叉排序树**：左子树所有节点 < 根节点 < 右子树所有节点

2. 递归遍历时常会漏掉递归终止条件
   - 必须检查 `if node is None: return`

3. 树的高度、深度、层数等概念也容易混淆
   - **深度**：从根到该节点（从上往下）
   - **高度**：从该节点到叶子（从下往上）
   - **层数**：深度相同的节点在同一层

4. 二叉搜索树的退化问题
   - 插入有序数据时会退化成链表
   - 需要使用平衡树（AVL、红黑树）来解决

## 练习提示
1. 学习遍历时，先在纸上画树，再手动模拟访问顺序
2. 实现计算树的高度的函数：`tree_height = 1 + max(left_height, right_height)`
3. 实现二叉搜索树的插入和查找操作
4. 练习根据遍历序列还原二叉树
5. 判断一棵树是否是完全二叉树

## 复杂度与考点
### 时间复杂度
- 二叉树遍历：`O(n)`，因为每个结点会被访问一次
- 二叉搜索树查找：
  - 理想平衡情况：`O(log n)`
  - 退化成链表：`O(n)`

### 考试重点
1. 给定遍历序列还原树
2. 判断完全二叉树
3. 计算结点度和树高
4. 二叉搜索树的性质和操作
5. 不同遍历方式的应用场景

### 空间复杂度
- 递归遍历：`O(h)`，h 为树的高度（递归栈空间）
- 层序遍历：`O(w)`，w 为树的最大宽度（队列空间）
