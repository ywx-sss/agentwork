# 数据结构课程知识库

本知识库采用**本地资料 + 网页链接**双轨并行的模式，确保知识的准确性和丰富性。

## 📚 本地课程资料

### 基础数据结构

#### 1. 栈与队列 [stack_queue.md](./stack_queue.md)
- **内容**：栈（LIFO）和队列（FIFO）的定义、原理、实现和应用
- **核心知识点**：
  - 栈的基本操作（push、pop、peek）
  - 队列的基本操作（enqueue、dequeue、front）
  - 循环队列的实现
  - 括号匹配、表达式求值等应用
  - 用栈实现队列、用队列实现栈
- **代码示例**：栈实现、队列实现、循环队列、经典应用题
- **网页补充**：[线性数据结构 - 栈和队列部分](https://www.runoob.com/data-structures/dsa-linear-data-structures.html)

#### 2. 链表 [linked_list.md](./linked_list.md)
- **内容**：单向链表、双向链表、循环链表的实现和操作
- **核心知识点**：
  - 链表的插入、删除、遍历操作
  - 链表 vs 数组的对比
  - 快慢指针技巧
  - 经典算法题（反转链表、环检测、中间节点）
- **代码示例**：单向链表、双向链表、经典算法题实现
- **网页补充**：[线性数据结构 - 链表部分](https://www.runoob.com/data-structures/dsa-linear-data-structures.html)

#### 3. 树与二叉树 [tree.md](./tree.md)
- **内容**：树的基本概念、二叉树遍历、二叉搜索树
- **核心知识点**：
  - 树的基本术语和性质
  - 四种遍历方式（前序、中序、后序、层序）
  - 二叉搜索树的插入和查找
  - 树的实际应用场景
- **代码示例**：二叉树节点定义、遍历算法、二叉搜索树实现
- **网页补充**：[树形结构基础](https://www.runoob.com/data-structures/dsa-tree.html)

#### 4. 图 [graph.md](./graph.md)
- **内容**：图的基本概念、存储方式、遍历算法
- **核心知识点**：
  - 图的分类（有向/无向、有权/无权）
  - 邻接矩阵和邻接表
  - BFS 和 DFS 遍历算法
  - 图的实际应用
- **代码示例**：BFS、DFS 实现、邻接矩阵和邻接表表示
- **网页补充**：[图论结构基础](https://www.runoob.com/data-structures/dsa-graph.html)

### 高级数据结构

#### 5. 哈希表 [hash_table.md](./hash_table.md)
- **内容**：哈希表的原理、哈希函数设计、冲突解决方法
- **核心知识点**：
  - 哈希函数的设计原则
  - 链地址法和开放定址法
  - 负载因子和扩容机制
  - 哈希表的性能分析
- **代码示例**：链地址法实现、单词计数器应用
- **网页补充**：[哈希表详解](https://www.runoob.com/data-structures/dsa-hash-table.html)

#### 6. 高级树结构 [advanced_tree.md](./advanced_tree.md)
- **内容**：AVL 树、红黑树、B 树、B+ 树
- **核心知识点**：
  - AVL 树的平衡因子和旋转操作
  - 红黑树的五项核心规则
  - B 树和 B+ 树的区别
  - 数据库索引的应用
- **代码示例**：AVL 树节点定义、旋转操作、红黑树节点定义
- **网页补充**：[高级树结构](https://www.runoob.com/data-structures/dsa-advanced-tree.html)

#### 7. 高级图算法 [advanced_graph.md](./advanced_graph.md)
- **内容**：最短路径、最小生成树、拓扑排序
- **核心知识点**：
  - Dijkstra 算法（单源最短路径）
  - Prim 算法（最小生成树）
  - Kahn 算法（拓扑排序）
  - 算法对比和应用场景
- **代码示例**：Dijkstra、Prim、拓扑排序的完整实现
- **网页补充**：[高级图算法](https://www.runoob.com/data-structures/dsa-advanced-graph.html)

#### 8. 堆存储 [heap_storage.md](./heap_storage.md)
- **内容**：堆的定义、完全二叉树、优先队列
- **核心知识点**：
  - 最大堆和最小堆
  - 堆的数组表示方法
  - 上浮和下沉操作
  - Top K 问题应用
- **代码示例**：最大堆实现、Python heapq 使用、Top K 问题
- **网页补充**：[堆的基本存储](https://www.runoob.com/data-structures/heap-storage.html)

### 其他主题

#### 9. 排序算法 [sorting.md](./sorting.md)
- **内容**：各种经典排序算法
- **网页补充**：待补充

#### 10. 递归与搜索 [recursion_search.md](./recursion_search.md)
- **内容**：递归原理、搜索算法
- **网页补充**：待补充

## 🌐 网页链接资源

### 菜鸟教程 Runoob 数据结构系列

| 主题 | 网址 | 对应本地文件 |
|------|------|-------------|
| 线性数据结构 | https://www.runoob.com/data-structures/dsa-linear-data-structures.html | stack_queue.md, linked_list.md |
| 哈希表 | https://www.runoob.com/data-structures/dsa-hash-table.html | hash_table.md |
| 树形结构 | https://www.runoob.com/data-structures/dsa-tree.html | tree.md |
| 图论结构 | https://www.runoob.com/data-structures/dsa-graph.html | graph.md |
| 高级树结构 | https://www.runoob.com/data-structures/dsa-advanced-tree.html | advanced_tree.md |
| 高级图算法 | https://www.runoob.com/data-structures/dsa-advanced-graph.html | advanced_graph.md |
| 堆存储 | https://www.runoob.com/data-structures/heap-storage.html | heap_storage.md |

## 📊 知识库统计

### 本地资料覆盖
- ✅ 栈与队列
- ✅ 链表
- ✅ 树与二叉树
- ✅ 图
- ✅ 哈希表
- ✅ 高级树结构
- ✅ 高级图算法
- ✅ 堆存储
- ⏳ 排序算法
- ⏳ 递归与搜索

### 网页链接覆盖
- ✅ 7 个核心知识点的官方教程链接
- ✅ 所有链接均经过验证，确保有效
- ✅ 网页内容作为本地资料的补充和扩展

## 🎯 使用建议

### 学习路径
1. **基础阶段**：先学习 stack_queue.md、linked_list.md
2. **核心阶段**：深入学习 tree.md、graph.md、hash_table.md
3. **进阶阶段**：挑战 advanced_tree.md、advanced_graph.md
4. **应用阶段**：结合 heap_storage.md 解决实际问题

### 学习方法
1. **阅读本地资料**：理解核心概念和原理
2. **查看代码示例**：动手实现数据结构
3. **参考网页链接**：获取更多例题和详细解释
4. **完成练习**：巩固所学知识

### RAG 检索优化
知识库已配置完善的主题关键词映射：
- 每个主题都有精准的关键词标签
- 支持模糊匹配和语义检索
- 本地资料和网页链接双重检索

## 🔄 更新机制

### 本地资料更新
- 定期补充新的知识点
- 增加代码示例和练习题
- 优化知识结构和组织

### 网页链接更新
- 验证链接有效性
- 清理无效链接（404 页面）
- 添加新的优质资源链接

### 质量保证
- ✅ 所有内容经过人工审核
- ✅ 网页链接定期验证
- ✅ 本地资料持续优化
- ✅ 错误内容及时清理

---

**最后更新**：2026-04-24
**资料数量**：10 个本地文件 + 7 个网页链接
**覆盖范围**：数据结构核心知识点全覆盖
