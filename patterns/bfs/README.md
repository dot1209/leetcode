# BFS

## When to Use
- 找「最短步數 / 最短距離」且每一步成本相同（unweighted graph 或 grid 上下左右一步算 1）
- 從一個來源（或多個來源）一層一層往外擴散
- 題目敘述出現：shortest path、minimum steps、最短時間、層序遍歷、最近的某種東西
- 與 DFS 的差別：BFS 用 queue 按距離分層、第一次碰到目標就是最短；DFS 用 stack/遞迴深入到底，**不保證**最短

BFS 的核心保證：**邊權都相等時，第一次到達某節點所經過的邊數就是最短距離**。一旦邊權不等（草地 1、沼澤 3）這個保證就失效，要改用 Dijkstra；若只有 0/1 兩種邊權則可用 0-1 BFS（deque）。

## Typical Complexity
**Time:** O(V + E)。每個節點最多進 queue 一次（被 visited 標記擋下），每條邊最多被檢查一次。Grid 上常見寫法是 O(m·n)：節點 m·n 個、每個節點最多檢查 4 個鄰居，總邊數 4·m·n。
**Space:** O(V)。queue 在最壞情況下可能同時裝下整層的節點；`visited` 結構也是 O(V)。

## General Template
```cpp
queue<State> q;
q.push(start);
visited.insert(start);
int steps = 0;
while (!q.empty()) {
    // only needed when counting levels
    int sz = q.size();
    while (sz--) {
        auto cur = q.front(); q.pop();
        if (isGoal(cur)) return steps;
        for (auto& nxt : neighbors(cur)) {
            if (visited.count(nxt)) continue;
            visited.insert(nxt);
            q.push(nxt);
        }
    }
    steps++;
}
return -1;
```

兩個關鍵動作：**push 前標 visited**（不是 pop 後才標，否則同一節點會被多次入隊）、**第一次碰到就是答案**（後續再碰到不會更短，直接 skip）。

## Common Variations
- [Multi-source BFS](multi-source-bfs.md) — 一開始就把多個起點一起塞進 queue，同步往外擴散
