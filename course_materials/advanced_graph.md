# 高级图算法

## 定义
高级图算法是解决复杂图问题的强大工具，包括最短路径算法、最小生成树算法、拓扑排序等，广泛应用于社交网络分析、地图导航、物流配送、网页排名等领域。

主要包括：
- **Dijkstra 算法**：单源最短路径问题
- **Prim 算法**：最小生成树问题
- **Kahn 算法**：拓扑排序
- **Kruskal 算法**：最小生成树的另一种解法

## 原理

### Dijkstra 算法：单源最短路径
**问题描述**：在带非负权重的图中，找到从起点到所有其他节点的最短路径。

**核心思想**（贪心算法）：
1. 维护一个"已知最短距离"的集合
2. 每次从"未知区域"中挑选一个当前离起点距离最短的节点
3. 确认它的最短距离，并用它更新所有邻居的"预估最短距离"
4. 重复直到所有节点的最短距离都被确认

**算法步骤**：
1. 初始化：起点距离为 0，其他节点距离为无穷大
2. 使用优先队列（最小堆），总是取出当前距离最小的节点
3. 用该节点更新其邻居的距离
4. 重复直到队列为空

**时间复杂度**：O((V+E) log V)，使用优先队列

### Prim 算法：最小生成树
**问题描述**：在带权重的连通无向图中，找到连接所有节点的边集，使得总权重最小。

**核心思想**（贪心算法）：
1. 从任意节点开始，初始化树只包含该节点
2. 在所有连接树内部和外部的边中，选择权重最小的边
3. 将该边及其连接的外部节点加入树中
4. 重复直到所有节点都被包含

**算法步骤**：
1. 从任意节点开始，标记为已访问
2. 将该节点的所有边加入优先队列
3. 取出权重最小的边，如果连接的节点未访问，则加入 MST
4. 将新节点的所有边加入队列
5. 重复直到所有节点都被访问

**时间复杂度**：O((V+E) log V)

### 拓扑排序：处理依赖关系
**问题描述**：对有向无环图（DAG）的顶点进行线性排序，使得对于任何有向边 u->v，u 在排序中都排在 v 之前。

**Kahn 算法**（基于入度）：
1. 找到所有入度为 0 的节点（没有前置依赖）
2. 将这些节点放入队列，并输出到排序结果
3. "移除"节点后，更新其所有邻居的入度（减 1）
4. 如果某个邻居的入度变为 0，加入队列
5. 重复直到队列为空
6. 如果输出的节点数等于总节点数，排序成功；否则存在环

**时间复杂度**：O(V+E)

## 示例

### Dijkstra 算法实现
```python
import heapq

def dijkstra(graph, start):
    """
    graph: 字典表示的邻接表 {节点：[(邻居 1, 权重 1), ...]}
    start: 起始节点
    """
    shortest_distances = {node: float('inf') for node in graph}
    shortest_distances[start] = 0
    
    # 优先队列：(当前距离，节点)
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # 跳过旧数据
        if current_distance > shortest_distances[current_node]:
            continue
        
        # 更新邻居
        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            if distance < shortest_distances[neighbor]:
                shortest_distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return shortest_distances

# 测试
test_graph = {
    'A': [('B', 4), ('C', 2)],
    'B': [('C', 1), ('D', 5)],
    'C': [('B', 1), ('D', 8), ('E', 10)],
    'D': [('E', 2)],
    'E': []
}

distances = dijkstra(test_graph, 'A')
# 结果：A:0, B:3, C:2, D:8, E:10
```

### Prim 算法实现
```python
import heapq

def prim_mst(graph):
    """
    graph: 字典表示的无向图邻接表
    """
    start_node = list(graph.keys())[0]
    visited = set([start_node])
    
    # 优先队列：(边权重，from_node, to_node)
    edges = [(weight, start_node, neighbor) 
             for neighbor, weight in graph[start_node]]
    heapq.heapify(edges)
    
    total_weight = 0
    mst_edges = []
    
    while edges:
        weight, from_node, to_node = heapq.heappop(edges)
        
        if to_node not in visited:
            visited.add(to_node)
            total_weight += weight
            mst_edges.append((from_node, to_node, weight))
            
            for neighbor, w in graph[to_node]:
                if neighbor not in visited:
                    heapq.heappush(edges, (w, to_node, neighbor))
    
    return total_weight, mst_edges
```

### 拓扑排序实现
```python
from collections import deque

def topological_sort_kahn(graph):
    """
    graph: 字典表示的有向图邻接表
    返回：拓扑排序结果列表，如果存在环则返回 None
    """
    # 计算入度
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] = in_degree.get(neighbor, 0) + 1
    
    # 初始化队列
    queue = deque([node for node in in_degree if in_degree[node] == 0])
    topo_order = []
    
    # 处理队列
    while queue:
        current_node = queue.popleft()
        topo_order.append(current_node)
        
        for neighbor in graph.get(current_node, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # 检查是否所有节点都被排序
    if len(topo_order) == len(graph):
        return topo_order
    else:
        return None  # 存在环

# 课程依赖示例
course_graph = {
    '程序设计': ['数据结构', '算法'],
    '数据结构': ['算法', '数据库'],
    '算法': ['机器学习'],
    '数据库': ['系统设计'],
    '数学': ['机器学习'],
    '机器学习': [],
    '系统设计': []
}

result = topological_sort_kahn(course_graph)
# 可能结果：程序设计 -> 数学 -> 数据结构 -> 算法 -> 数据库 -> 机器学习 -> 系统设计
```

## 易错点
1. **Dijkstra 算法**：
   - 不能处理负权重边（需要使用 Bellman-Ford 算法）
   - 优先队列中可能包含同一节点的多个旧版本，需要跳过
   - 距离更新条件判断错误

2. **Prim 算法**：
   - 忘记检查节点是否已访问
   - 无向图的边需要存储两次
   - 与 Dijkstra 算法混淆

3. **拓扑排序**：
   - 只适用于有向无环图（DAG）
   - 入度计算错误
   - 忘记检查是否存在环

## 练习提示
1. 手动模拟 Dijkstra 算法的执行过程
2. 比较 Prim 算法和 Kruskal 算法的差异
3. 使用拓扑排序解决课程安排问题
4. 修复 Dijkstra 算法中的常见 bug

## 复杂度与考点

### 算法对比
| 算法 | 主要用途 | 适用图类型 | 核心思想 | 时间复杂度 | 典型应用 |
|------|----------|------------|----------|------------|----------|
| Dijkstra | 单源最短路径 | 带非负权重的有向/无向图 | 贪心，每次扩展最近节点 | O((V+E) log V) | 地图导航、网络路由 |
| Prim | 最小生成树 | 带权重的连通无向图 | 贪心，每次并入最近节点 | O((V+E) log V) | 网络布线、电路板设计 |
| Kahn | 拓扑排序 | 有向无环图（DAG） | 基于入度，不断移除无依赖节点 | O(V+E) | 课程安排、构建系统依赖 |

### 考试重点
1. Dijkstra 算法的执行过程和代码实现
2. Prim 算法和 Kruskal 算法的区别
3. 拓扑排序的 Kahn 算法实现
4. 如何判断图中是否存在环
5. 算法的时间复杂度分析
6. 实际应用场景的选择

### 实际应用
1. **地图导航**：Dijkstra 算法找最短路径
2. **网络布线**：Prim 算法设计最小成本网络
3. **课程安排**：拓扑排序处理先修关系
4. **任务调度**：拓扑排序确定执行顺序
5. **社交网络**：分析用户关系和影响力
