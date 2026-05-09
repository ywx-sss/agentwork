# 堆存储

## 定义
堆（Heap）是计算机科学中一类特殊的数据结构的统称。堆通常是一个可以被看做一棵完全二叉树的数组对象。

堆满足以下两个核心性质：
1. **结构性**：堆总是一棵完全二叉树
2. **有序性**：堆中某个节点的值总是不大于或不小于其父节点的值

根据有序性的不同，堆分为：
- **最大堆（Max Heap）**：每个节点的值都大于或等于其子节点的值，根节点最大
- **最小堆（Min Heap）**：每个节点的值都小于或等于其子节点的值，根节点最小

## 原理

### 完全二叉树的数组表示
堆利用完全二叉树的结构来维护一组数据。完全二叉树的特点是：
- 除最后一层外，其它各层的结点数都达到最大个数
- 第 k 层所有的结点都连续集中在最左边

使用数组存储二叉堆的规律（假设索引从 1 开始）：
- `parent(i) = i / 2`（取整）- 父节点索引
- `left_child(i) = 2 * i` - 左子节点索引
- `right_child(i) = 2 * i + 1` - 右子节点索引

如果索引从 0 开始：
- `parent(i) = (i - 1) / 2`（取整）
- `left_child(i) = 2 * i + 1`
- `right_child(i) = 2 * i + 2`

### 堆的基本操作
#### 1. 插入（Push）
1. 将新元素添加到数组末尾
2. 执行"上浮"（Sift Up）操作，与父节点比较并交换，直到满足堆性质

#### 2. 删除堆顶（Pop）
1. 用数组末尾元素替换堆顶元素
2. 删除数组末尾元素
3. 执行"下沉"（Sift Down）操作，与较大的子节点（最大堆）或较小的子节点（最小堆）交换，直到满足堆性质

#### 3. 获取堆顶
直接返回数组的第一个元素（索引 0 或 1）

### 时间复杂度
| 操作 | 时间复杂度 |
|------|------------|
| 插入 | O(log n) |
| 删除堆顶 | O(log n) |
| 获取堆顶 | O(1) |
| 建堆 | O(n) |

### 堆 vs 优先队列
堆是实现优先队列的最佳数据结构：

| 实现方式 | 入队时间 | 出队时间 |
|----------|----------|----------|
| 普通数组 | O(1) | O(n) |
| 顺序数组 | O(n) | O(1) |
| 堆 | O(log n) | O(log n) |

## 示例

### Python 实现最大堆
```python
class MaxHeap:
    def __init__(self):
        self.heap = []
    
    def parent(self, i):
        return (i - 1) // 2
    
    def left_child(self, i):
        return 2 * i + 1
    
    def right_child(self, i):
        return 2 * i + 2
    
    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
    
    def insert(self, value):
        """插入元素"""
        self.heap.append(value)
        self._sift_up(len(self.heap) - 1)
    
    def _sift_up(self, i):
        """上浮操作"""
        while i > 0:
            parent_idx = self.parent(i)
            if self.heap[i] > self.heap[parent_idx]:
                self.swap(i, parent_idx)
                i = parent_idx
            else:
                break
    
    def extract_max(self):
        """删除并返回堆顶元素"""
        if not self.heap:
            return None
        
        # 保存堆顶
        max_val = self.heap[0]
        
        # 用末尾元素替换堆顶
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        
        # 下沉操作
        if self.heap:
            self._sift_down(0)
        
        return max_val
    
    def _sift_down(self, i):
        """下沉操作"""
        max_idx = i
        
        while True:
            left = self.left_child(i)
            right = self.right_child(i)
            
            # 找到 i、left、right 中最大的
            if left < len(self.heap) and self.heap[left] > self.heap[max_idx]:
                max_idx = left
            
            if right < len(self.heap) and self.heap[right] > self.heap[max_idx]:
                max_idx = right
            
            # 如果最大值不是当前节点，交换并继续
            if max_idx != i:
                self.swap(i, max_idx)
                i = max_idx
            else:
                break
    
    def get_max(self):
        """获取堆顶元素"""
        return self.heap[0] if self.heap else None
    
    def size(self):
        return len(self.heap)
    
    def is_empty(self):
        return len(self.heap) == 0

# 测试
heap = MaxHeap()
heap.insert(10)
heap.insert(20)
heap.insert(15)
heap.insert(30)
heap.insert(25)

print(f"堆顶元素：{heap.get_max()}")  # 30
print(f"删除堆顶：{heap.extract_max()}")  # 30
print(f"新的堆顶：{heap.get_max()}")  # 25
```

### Python 使用内置 heapq（最小堆）
```python
import heapq

# 创建最小堆
min_heap = []
heapq.heapify(min_heap)

# 插入元素
heapq.heappush(min_heap, 10)
heapq.heappush(min_heap, 5)
heapq.heappush(min_heap, 20)

# 获取堆顶
print(f"最小值：{min_heap[0]}")  # 5

# 删除堆顶
min_val = heapq.heappop(min_heap)
print(f"删除的最小值：{min_val}")  # 5

# 模拟最大堆（使用负数）
max_heap = []
heapq.heappush(max_heap, -10)
heapq.heappush(max_heap, -5)
heapq.heappush(max_heap, -20)
max_val = -heapq.heappop(max_heap)
print(f"最大值：{max_val}")  # 20
```

### 应用示例：Top K 问题
找出数组中最大的 K 个元素：
```python
import heapq

def top_k_largest(nums, k):
    """使用最小堆找出最大的 K 个数"""
    if k <= 0:
        return []
    
    # 维护一个大小为 k 的最小堆
    min_heap = nums[:k]
    heapq.heapify(min_heap)
    
    for num in nums[k:]:
        if num > min_heap[0]:
            heapq.heapreplace(min_heap, num)
    
    return sorted(min_heap, reverse=True)

# 测试
nums = [3, 2, 1, 5, 6, 4]
k = 2
result = top_k_largest(nums, k)
print(f"最大的{k}个数：{result}")  # [6, 5]
```

## 易错点
1. **索引计算错误**：父节点、子节点的索引公式记混
2. **边界条件**：空堆、单元素堆的处理
3. **上浮和下沉**：
   - 上浮时忘记判断是否到达根节点
   - 下沉时忘记检查子节点是否存在
   - 最大堆和最小堆的比较方向搞反
4. **数组索引**：从 0 开始还是从 1 开始的索引差异

## 练习提示
1. 手动模拟堆的插入和删除过程
2. 实现最大堆和最小堆的完整操作
3. 使用堆解决 Top K 问题
4. 理解为什么建堆的时间复杂度是 O(n)
5. 练习使用 Python 的 heapq 模块

## 复杂度与考点

### 时间复杂度分析
- **插入操作**：O(log n)
  - 最坏情况下需要从叶子节点上浮到根节点
  - 树的高度为 log n
  
- **删除堆顶**：O(log n)
  - 最坏情况下需要从根节点下沉到叶子节点
  
- **建堆**：O(n)
  - 从最后一个非叶子节点开始，依次执行下沉操作
  - 虽然是 n/2 次下沉，但大部分节点的高度很小
  - 通过数学推导可得总复杂度为 O(n)

### 空间复杂度
- O(n)，需要数组存储所有元素

### 考试重点
1. 堆的性质和完全二叉树的特点
2. 堆的数组表示方法（索引计算）
3. 插入和删除操作的实现
4. 上浮和下沉操作的细节
5. 堆排序算法
6. 优先队列的应用

### 实际应用场景
1. **优先队列**：任务调度、事件驱动模拟
2. **堆排序**：时间复杂度 O(n log n) 的原地排序
3. **Top K 问题**：找最大/最小的 K 个元素
4. **中位数问题**：使用最大堆和最小堆维护数据流的中位数
5. **合并 K 个有序链表**：使用最小堆维护 K 个链表的当前最小值
6. **定时任务**：按照执行时间排序的任务队列
