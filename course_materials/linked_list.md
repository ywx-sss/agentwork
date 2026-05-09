# 链表

## 定义
链表（Linked List）是一种逻辑上连续、物理上不一定连续的线性结构。
每个结点通常包含数据域和指针域，单链表中的指针指向后继结点。

链表像是一串手拉手的人：
- **头节点**：链表的第一个节点（或头结点）
- **尾节点**：最后一个节点，指针指向 NULL
- **中间节点**：既有前驱也有后继的节点

## 原理
链表不要求存储空间连续，因此插入和删除操作灵活。
若已知待操作位置的前驱结点，则插入和删除只需要修改少量指针。
链表不支持像数组那样的随机访问，查找某个位置通常需要从头遍历。

### 链表的类型
1. **单向链表**：每个节点只有一个指针，指向后继节点
2. **双向链表**：每个节点有两个指针，分别指向前驱和后继节点
3. **循环链表**：尾节点的指针指向头节点，形成环状
4. **带头结点的链表**：在第一个数据节点前增加一个头结点，简化操作

### 链表 vs 数组
| 特性 | 数组 | 链表 |
|------|------|------|
| 存储方式 | 连续内存 | 分散内存，通过指针连接 |
| 访问方式 | 随机访问（通过索引） | 顺序访问（必须遍历） |
| 插入/删除效率 | 尾部快，中间/头部慢（需移动元素） | 已知位置时快（只需改指针） |
| 大小 | 固定（静态数组） | 动态 |
| 空间效率 | 高 | 需要额外指针空间 |

### 链表的基本操作
#### 1. 插入操作
在节点 p 后插入新节点 s：
```python
s.next = p.next  # 先连后继
p.next = s       # 再连前驱
```

#### 2. 删除操作
删除节点 p 的后继节点 q：
```python
q = p.next           # 找到要删除的节点
p.next = q.next      # 绕过 q 连接
del q                # 释放内存（Python 自动垃圾回收）
```

#### 3. 遍历操作
```python
current = head
while current is not None:
    print(current.data)
    current = current.next
```

## 示例
### Python 实现单向链表
```python
class ListNode:
    """链表节点类"""
    def __init__(self, data):
        self.data = data  # 数据域
        self.next = None  # 指针域

class LinkedList:
    """单向链表类"""
    def __init__(self):
        self.head = None  # 头指针
    
    def append(self, data):
        """在链表末尾添加节点"""
        new_node = ListNode(data)
        if not self.head:  # 如果链表为空
            self.head = new_node
            return
        
        last_node = self.head
        while last_node.next:  # 遍历到最后一个节点
            last_node = last_node.next
        last_node.next = new_node
    
    def prepend(self, data):
        """在链表头部添加节点"""
        new_node = ListNode(data)
        new_node.next = self.head
        self.head = new_node
    
    def insert_after(self, prev_data, data):
        """在指定值后插入节点"""
        current = self.head
        while current:
            if current.data == prev_data:
                new_node = ListNode(data)
                new_node.next = current.next
                current.next = new_node
                return
            current = current.next
    
    def delete(self, key):
        """删除第一个值为 key 的节点"""
        current = self.head
        
        # 如果要删除的是头节点
        if current and current.data == key:
            self.head = current.next
            current = None
            return
        
        # 寻找要删除节点的前驱
        prev = None
        while current and current.data != key:
            prev = current
            current = current.next
        
        if current is None:  # 没找到
            return
        
        # 绕过要删除的节点
        prev.next = current.next
        current = None
    
    def search(self, key):
        """查找值为 key 的节点"""
        current = self.head
        while current:
            if current.data == key:
                return True
            current = current.next
        return False
    
    def print_list(self):
        """打印链表"""
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("NULL")

# 测试
ll = LinkedList()
ll.append(1)
ll.append(2)
ll.append(3)
ll.prepend(0)
ll.print_list()  # 输出：0 -> 1 -> 2 -> 3 -> NULL

ll.delete(2)
ll.print_list()  # 输出：0 -> 1 -> 3 -> NULL
```

### 双向链表实现
```python
class DoublyListNode:
    """双向链表节点"""
    def __init__(self, data):
        self.data = data
        self.prev = None  # 指向前驱
        self.next = None  # 指向后继

class DoublyLinkedList:
    """双向链表类"""
    def __init__(self):
        self.head = None
        self.tail = None
    
    def append(self, data):
        """在末尾添加节点"""
        new_node = DoublyListNode(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
    
    def delete(self, key):
        """删除节点"""
        current = self.head
        while current:
            if current.data == key:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                
                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                return
            current = current.next
```

### 经典算法题
#### 1. 反转链表
```python
def reverse_list(head):
    """反转单向链表"""
    prev = None
    current = head
    while current:
        next_node = current.next  # 保存后继
        current.next = prev       # 反转指针
        prev = current            # 移动 prev
        current = next_node       # 移动 current
    return prev
```

#### 2. 检测环
```python
def has_cycle(head):
    """使用快慢指针检测链表是否有环"""
    if not head or not head.next:
        return False
    
    slow = head
    fast = head.next
    
    while fast and fast.next:
        if slow == fast:
            return True
        slow = slow.next
        fast = fast.next.next
    
    return False
```

#### 3. 找到中间节点
```python
def find_middle(head):
    """使用快慢指针找到中间节点"""
    slow = head
    fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    return slow
```

## 易错点
1. **带头结点 vs 不带头结点**
   - 带头结点：第一个数据节点在 head.next，简化边界处理
   - 不带头结点：head 直接指向第一个数据节点

2. **指针修改顺序**
   - 插入时：先连后继，再连前驱
   - 删除时：先保存要删除的节点，再修改指针

3. **边界条件**
   - 空链表的处理
   - 只有一个节点的情况
   - 操作头节点或尾节点的特殊情况

4. **循环链表**
   - 遍历终止条件是回到起点
   - 注意避免死循环

5. **内存泄漏**
   - 删除节点后要释放内存（C/C++ 需要注意）
   - Python 有自动垃圾回收

## 练习提示
1. 遇到链表题时，先画出结点和指针变化过程
2. 使用快慢指针解决中间节点、环检测等问题
3. 练习反转链表、合并有序链表等经典题目
4. 理解递归和迭代两种解法
5. 注意边界条件和空指针检查

## 复杂度与考点
### 时间复杂度
| 操作 | 时间复杂度 |
|------|------------|
| 访问元素 | O(n) - 需要遍历 |
| 头部插入 | O(1) |
| 尾部插入 | O(n) - 需要遍历到尾部 |
| 中间插入 | O(n) - 需要找到位置 |
| 删除元素 | O(n) - 需要找到位置 |

### 空间复杂度
- 单向链表：O(n)，每个节点一个指针
- 双向链表：O(n)，每个节点两个指针

### 考试重点
1. 链表的插入和删除操作
2. 链表反转
3. 环检测问题
4. 快慢指针的应用
5. 合并两个有序链表
6. 判断回文链表
7. 删除倒数第 N 个节点

### 实际应用
1. **实现其他数据结构**：栈、队列、哈希表（链地址法）
2. **动态内存分配**：操作系统内存管理
3. **浏览器历史记录**：前进后退功能
4. **音乐播放列表**：歌曲的顺序管理
5. **图的邻接表表示**：存储图的边
