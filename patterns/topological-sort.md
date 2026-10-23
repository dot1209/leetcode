# Topological Sort

## When to Use
- 有向圖的 dependency／prerequisite，必須輸出符合先後約束的順序。
- 需要判斷是否存在 directed cycle，或找出所有工作可執行的先後次序。
- Kahn's Algorithm 適合從 indegree = 0 的節點開始；DFS Postorder 是另一種值得掌握的解法。

## Typical Complexity
**Time:** O(V + E) — 建圖後，每個節點最多出隊一次，每條邊隨來源節點的 adjacency list 最多處理一次。
**Space:** O(V + E) — adjacency list 儲存 V 個節點與 E 條邊，indegree／queue／result 各需要 O(V)。

## Core Invariants
### Kahn's Algorithm
- 對 prerequisite `[a, b]` 建立 `b -> a`，同時執行 `indegree[a]++`。注意 `graph[u].size()` 是 outdegree，不是 indegree。
- Queue 中的節點，其尚未處理的 incoming edges 為零；取出節點時，所有 prerequisites 已經完成。
- 每條邊只存放在來源節點的 adjacency list。節點只會在 indegree 從正數降至零時入隊一次，所以每條邊只會掃描一次。
- 完成後若 `processedCount != V`，代表有 cycle，無法產生完整拓樸順序。
- 若只要合法順序，不需要 BFS level；若每個學期可同時修任意數量的課，則一層 BFS 對應一個學期。

### DFS Postorder
- 對 `u -> v`，先完成 `v` 再將 `u` 加入 postorder，最後 reverse 即為拓樸順序。
- 三色狀態：0 = unvisited，1 = visiting（目前遞迴路徑上），2 = finished。Directed Graph 遇到 state = 1 表示 back edge／cycle；遇到 state = 2 不是 cycle。
- Undirected Graph 通常改用 visited + parent：跳過返回 parent 的邊，若遇到其他 visited 節點則有 cycle。此寫法假設 simple graph；若允許 parallel edges，應追蹤 parent edge ID。

## Template Code
```cpp
vector<vector<int>> graph(n);
vector<int> indegree(n, 0);
for (const auto& pre : prerequisites) {
    graph[pre[1]].push_back(pre[0]);
    ++indegree[pre[0]];
}
queue<int> q;
for (int u = 0; u < n; ++u) {
    if (indegree[u] == 0) q.push(u);
}
vector<int> order;
while (!q.empty()) {
    int u = q.front();
    q.pop();
    order.push_back(u);
    for (int v : graph[u]) {
        if (--indegree[v] == 0) q.push(v);
    }
}
if (order.size() != n) return {};
return order;
```

## Pitfalls
- 將 `[a, b]` 誤建成 `a -> b`，會得到反向修課順序。
- `graph[i].size()` 是 outdegree；indegree 應在建圖時針對目的節點增加。
- 圖可能只有局部 cycle，不能只檢查 Queue 初始是否為空；必須比較完成節點數與 V。
- `vector<vector<int>> graph(V)` 是 adjacency list，空間 O(V + E)；`vector<vector<int>>(V, vector<int>(V))` 才是 O(V²) 的 adjacency matrix。
- 若用 `unordered_set` 去重，indegree 也必須只在成功插入新邊時增加；若題目保證無重複邊，`vector<vector<int>>` 較簡單。
- DFS 的 state = 1 表示目前遞迴路徑上的節點；不能把所有 visited 節點都視為 directed cycle。

---

## Problems

### [[210] Course Schedule II](../problems/topological-sort/course_schedule_ii.md)
**Complexity:** Time O(V + E), Space O(V + E)
- **Trigger:** 依 prerequisites 輸出合法修課順序，若有 directed cycle 則回傳空陣列。
- **Insight:** 建立 `b -> a`，由 indegree = 0 的節點開始逐步解除 dependency。
- **Pitfall:** 不可用 adjacency list 長度當 indegree；最後要確認輸出數量等於 numCourses。
