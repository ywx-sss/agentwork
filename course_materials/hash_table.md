# 哈希表

## 定义
哈希表（Hash Table），也叫散列表，是一种极其高效的数据结构。哈希表能在平均情况下，以接近 O(1) 的时间复杂度进行数据的插入、删除和查找。

哈希表就像是一个智能的储物柜系统：
- 传统储物柜：你需要记住每个物品放在哪个柜子里（线性查找）
- 智能储物柜：你告诉管理员物品名称，他直接告诉你柜子编号（哈希查找）

核心思想：通过哈希函数将键（Key）转换为数组索引，实现快速访问。

## 原理
哈希表是一种通过键（Key）来直接访问值（Value）的数据结构，它利用一个叫做哈希函数的魔法公式，把任意大小的键转换成一个固定大小的数字（哈希值或哈希码），然后用这个哈希值作为数组的索引。

### 核心组件
1. **键（Key）**：你要存储和查找数据时使用的标识符
2. **值（Value）**：与键相关联的实际数据
3. **哈希函数（Hash Function）**：将键映射到数组索引的数学函数

### 哈希函数设计
好的哈希函数特性：
- **确定性**：相同输入总是产生相同输出
- **均匀分布**：输出均匀分布在哈希表范围内
- **高效计算**：计算过程简单快速
- **雪崩效应**：输入微小变化导致输出巨大变化

常见哈希函数：
- 除法取余法：hash = key % table_size（整数键）
- 乘法取整法：hash = floor(key * A % 1 * table_size)（浮点数键）
- 数字分析法：分析数字的分布规律（特定模式数据）
- 平方取中法：hash = (key * key) // 10^(n/2) % table_size（数字键）
- 字符串哈希：逐字符处理（字符串键）

### 冲突解决方法
#### 1. 链地址法（Separate Chaining）
每个哈希桶维护一个链表：
- 插入：在对应链表头部添加，O(1)
- 查找：在对应链表中搜索，O(k)，k 为链表长度
- 删除：在对应链表中删除，O(k)

#### 2. 开放定址法（Open Addressing）
所有元素都存储在数组本身中：
- **线性探测**：h, h+1, h+2, ...（简单易实现，容易聚集）
- **二次探测**：h, h+1², h+2², ...（减少聚集，可能无法探测所有位置）
- **双重哈希**：h, h+hash2(key), h+2*hash2(key), ...（分布均匀，计算复杂）

## 示例
### Python 实现 - 链地址法
```python
class HashTableChaining:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]
    
    def _hash(self, key):
        return hash(key) % self.size
    
    def insert(self, key, value):
        index = self._hash(key)
        bucket = self.table[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
    
    def get(self, key):
        index = self._hash(key)
        bucket = self.table[index]
        for k, v in bucket:
            if k == key:
                return v
        return None
```

### 应用示例：单词计数器
统计文本中每个单词出现的次数：
```python
word_counter = HashTableChaining(size=10)
text = "the quick brown fox jumps over the lazy dog the dog is not lazy at all"
words = text.split()

for word in words:
    current_count = word_counter.get(word)
    if current_count is None:
        word_counter.insert(word, 1)
    else:
        word_counter.insert(word, current_count + 1)
```

## 易错点
1. **哈希冲突处理**：不同的键可能映射到同一索引
2. **负载因子**：元素数/数组大小，过高时性能下降
3. **扩容时机**：负载因子超过阈值（如 0.75）时需要扩容和重哈希
4. **删除操作**：开放定址法中删除较复杂，需特殊标记

## 练习提示
1. 实现一个完整的哈希表，支持插入、删除、查找操作
2. 比较链地址法和开放定址法的性能差异
3. 设计不同的哈希函数，测试其分布效果
4. 实现动态扩容功能

## 复杂度与考点
### 时间复杂度对比
| 操作 | 数组/链表 | 哈希表 |
|------|----------|--------|
| 查找 | O(n) | O(1) |
| 插入 | O(n) | O(1) |
| 删除 | O(n) | O(1) |

### 空间效率
- 链地址法：需要额外空间存储指针
- 开放定址法：所有数据在数组中，空间利用率可能更高

### 考试重点
1. 哈希函数的设计原则
2. 冲突解决方法的比较
3. 负载因子的计算和影响
4. 哈希表的性能分析

## 实际应用场景
1. **数据库索引**：快速查找记录
2. **缓存系统**：LRU 缓存、浏览器缓存
3. **集合成员检查**：判断元素是否在集合中
4. **对象属性存储**：Python 的 dict、Java 的 HashMap
5. **编译器符号表**：存储变量名和类型信息
