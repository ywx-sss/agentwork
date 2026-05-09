# 栈与队列

## 定义
栈（Stack）是一种后进先出（LIFO）的线性表，只允许在表尾进行插入和删除。
队列（Queue）是一种先进先出（FIFO）的线性表，通常在队尾插入，在队头删除。

栈就像是一叠盘子：
- 只能从顶部取放盘子
- 最后放上去的盘子最先被取用

队列就像是排队买票：
- 新来的人排在队尾
- 队头的人先买票离开
- 先来先服务

## 原理

### 栈的核心特性
栈的核心是"最近进入的元素最先出来"（LIFO - Last In First Out）。

**基本操作**：
- **push(入栈)**：在栈顶添加元素，O(1)
- **pop(出栈)**：移除栈顶元素，O(1)
- **peek(查看)**：查看栈顶元素但不移除，O(1)
- **isEmpty(判空)**：检查栈是否为空，O(1)

**应用场景**：
- 函数调用栈：记录函数调用的层次关系
- 括号匹配：检查表达式中的括号是否配对
- 表达式求值：中缀表达式转后缀表达式
- 深度优先搜索（DFS）：使用栈实现递归
- 浏览器前进后退：历史记录管理

### 队列的核心特性
队列的核心是"最早进入的元素最先出来"（FIFO - First In First Out）。

**基本操作**：
- **enqueue(入队)**：在队尾添加元素，O(1)
- **dequeue(出队)**：从队头移除元素，O(1)
- **front(查看队头)**：查看队头元素但不移除，O(1)
- **isEmpty(判空)**：检查队列是否为空，O(1)

**应用场景**：
- 任务调度：操作系统中的进程调度
- 广度优先搜索（BFS）：按层遍历
- 消息队列：异步通信缓冲
- 打印队列：管理打印任务
- 带宽限流：控制数据流速度

### 特殊队列
1. **循环队列**：通过取模运算实现首尾相连，解决假溢出问题
2. **双端队列（Deque）**：两端都可以插入和删除
3. **优先队列**：元素有优先级，优先级高的先出队（通常用堆实现）

## 示例

### Python 实现栈
```python
class Stack:
    """使用列表实现栈"""
    def __init__(self):
        self.items = []
    
    def push(self, item):
        """入栈"""
        self.items.append(item)
    
    def pop(self):
        """出栈"""
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def peek(self):
        """查看栈顶元素"""
        if not self.is_empty():
            return self.items[-1]
        return None
    
    def is_empty(self):
        """检查栈是否为空"""
        return len(self.items) == 0
    
    def size(self):
        """返回栈的大小"""
        return len(self.items)

# 应用：括号匹配检查
def is_balanced_parentheses(expression):
    """检查表达式中的括号是否匹配"""
    stack = Stack()
    matching_bracket = {')': '(', ']': '[', '}': '{'}
    
    for char in expression:
        if char in '([{':  # 左括号入栈
            stack.push(char)
        elif char in ')]}':  # 右括号
            if stack.is_empty():
                return False
            top_char = stack.pop()
            if matching_bracket[char] != top_char:
                return False
    
    return stack.is_empty()

# 测试
print(is_balanced_parentheses("((1+2)*3)"))  # True
print(is_balanced_parentheses("({[ ]})"))    # True
print(is_balanced_parentheses("((())"))      # False
print(is_balanced_parentheses(")( )"))       # False
```

### Python 实现队列
```python
from collections import deque

class Queue:
    """使用双端队列实现队列"""
    def __init__(self):
        self.items = deque()
    
    def enqueue(self, item):
        """入队"""
        self.items.append(item)
    
    def dequeue(self):
        """出队"""
        if not self.is_empty():
            return self.items.popleft()
        return None
    
    def front(self):
        """查看队头"""
        if not self.is_empty():
            return self.items[0]
        return None
    
    def is_empty(self):
        """检查队列是否为空"""
        return len(self.items) == 0
    
    def size(self):
        """返回队列大小"""
        return len(self.items)

# 应用：模拟打印任务
def simulate_print_queue(tasks):
    """模拟打印队列处理任务"""
    queue = Queue()
    
    # 所有任务入队
    for task in tasks:
        queue.enqueue(task)
        print(f"任务 '{task}' 已加入打印队列")
    
    # 处理打印任务
    print("\n开始打印...")
    while not queue.is_empty():
        current_task = queue.dequeue()
        print(f"正在打印：{current_task}")
    
    print("所有打印任务已完成")

# 测试
tasks = ["Alice 的简历.pdf", "Bob 的报告.doc", "Charlie 的图表.png"]
simulate_print_queue(tasks)
```

### 循环队列实现
```python
class CircularQueue:
    """循环队列实现"""
    def __init__(self, max_size):
        self.max_size = max_size
        self.data = [None] * max_size
        self.front = 0  # 指向队头元素
        self.rear = 0   # 指向队尾元素的下一个位置
        self.size = 0   # 当前元素个数
    
    def enqueue(self, item):
        """入队"""
        if self.is_full():
            raise Exception("队列已满")
        self.data[self.rear] = item
        self.rear = (self.rear + 1) % self.max_size
        self.size += 1
    
    def dequeue(self):
        """出队"""
        if self.is_empty():
            raise Exception("队列为空")
        item = self.data[self.front]
        self.data[self.front] = None
        self.front = (self.front + 1) % self.max_size
        self.size -= 1
        return item
    
    def is_empty(self):
        """队列为空：front == rear"""
        return self.size == 0
    
    def is_full(self):
        """队列已满：rear 的下一个位置是 front"""
        return self.size == self.max_size
    
    def get_front(self):
        """获取队头元素"""
        if not self.is_empty():
            return self.data[self.front]
        return None

# 测试
cq = CircularQueue(5)
cq.enqueue(1)
cq.enqueue(2)
cq.enqueue(3)
print(f"队头：{cq.get_front()}")  # 1
print(f"出队：{cq.dequeue()}")    # 1
cq.enqueue(4)  # 利用循环空间
cq.enqueue(5)
cq.enqueue(6)
```

### 经典应用题
#### 1. 用两个栈实现队列
```python
class QueueWithTwoStacks:
    def __init__(self):
        self.stack1 = Stack()  # 用于入队
        self.stack2 = Stack()  # 用于出队
    
    def enqueue(self, item):
        self.stack1.push(item)
    
    def dequeue(self):
        if self.stack2.is_empty():
            if self.stack1.is_empty():
                raise Exception("队列为空")
            # 将 stack1 的元素全部倒入 stack2
            while not self.stack1.is_empty():
                self.stack2.push(self.stack1.pop())
        return self.stack2.pop()
```

#### 2. 用两个队列实现栈
```python
class StackWithTwoQueues:
    def __init__(self):
        self.queue1 = Queue()
        self.queue2 = Queue()
    
    def push(self, item):
        # 总是往非空的队列中添加
        if self.queue1.is_empty():
            self.queue2.enqueue(item)
        else:
            self.queue1.enqueue(item)
    
    def pop(self):
        if self.queue1.is_empty() and self.queue2.is_empty():
            raise Exception("栈为空")
        
        # 将 n-1 个元素移到另一个队列
        if self.queue1.is_empty():
            while self.queue2.size() > 1:
                self.queue1.enqueue(self.queue2.dequeue())
            return self.queue2.dequeue()
        else:
            while self.queue1.size() > 1:
                self.queue2.enqueue(self.queue1.dequeue())
            return self.queue1.dequeue()
```

#### 3. 单调栈应用
```python
def next_greater_element(nums):
    """找到每个元素右边第一个比它大的元素"""
    n = len(nums)
    result = [-1] * n
    stack = []  # 存储索引，栈中元素对应的值单调递减
    
    for i in range(n):
        while stack and nums[i] > nums[stack[-1]]:
            idx = stack.pop()
            result[idx] = nums[i]
        stack.append(i)
    
    return result

# 测试
nums = [2, 1, 2, 4, 3]
print(next_greater_element(nums))  # [2, 2, 4, -1, -1]
```

## 易错点
1. **栈顶 vs 队头**
   - 栈顶：最后进入的元素位置
   - 队头：最先进入的元素位置

2. **循环队列的判空和判满**
   - 判空：`front == rear` 或 `size == 0`
   - 判满：`(rear + 1) % max_size == front` 或 `size == max_size`
   - 建议显式维护 size 变量

3. **栈的溢出问题**
   - 上溢：栈满时继续入栈
   - 下溢：栈空时继续出栈

4. **递归与栈的关系**
   - 递归本质上依赖系统调用栈
   - 深度过大会导致栈溢出
   - 可以用显式栈将递归改为迭代

5. **双端队列的使用**
   - Python 的 `collections.deque` 支持两端操作
   - 适合实现栈和队列

## 练习提示
1. 分析出栈序列是否合法时，模拟"入栈一步，必要时连续出栈"
2. 判断队列题目时，先明确入队和出队发生的位置
3. 练习括号匹配、表达式求值等经典栈应用
4. 理解循环队列的指针变化
5. 掌握用栈实现队列、用队列实现栈的方法

## 复杂度与考点
### 时间复杂度
| 操作 | 栈 | 队列 | 循环队列 |
|------|----|----|----------|
| 插入 | O(1) | O(1) | O(1) |
| 删除 | O(1) | O(1) | O(1) |
| 查找 | O(n) | O(n) | O(n) |

### 空间复杂度
- 顺序栈/队列：O(n)
- 链式栈/队列：O(n)

### 考试重点
1. 栈和队列的基本操作实现
2. 括号匹配问题
3. 表达式求值（中缀转后缀）
4. 循环队列的判空判满
5. 用栈实现队列、用队列实现栈
6. 单调栈的应用
7. BFS 和 DFS 中的栈和队列使用

### 实际应用
1. **编译器**：语法分析、表达式求值
2. **操作系统**：函数调用栈、进程调度
3. **浏览器**：前进后退、标签页管理
4. **消息系统**：消息队列、任务缓冲
5. **算法设计**：DFS、BFS、拓扑排序
6. **数据流处理**：滑动窗口、限流算法
