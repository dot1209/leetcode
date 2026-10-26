# BFS — Graph Traversal

## When to Use
- 題目不是要最短路，而是要從一個起點把整個 connected component 都走完。
- 常見需求：複製 graph、收集所有 reachable nodes、沿 adjacency list 傳播資訊，或在 grid 中尋找島嶼。
- 若 graph 保證 connected，從任一給定起點跑一次 BFS 就能遍歷所有節點；若不保證 connected，還需要從未訪問節點重新啟動 traversal。

這類題的核心不是 level，而是「每個節點只處理一次，所有 edge 都掃到」。對 clone 類問題，可以把 `original -> copy` mapping 同時當成 visited。

## Connected Component 的遍歷與屬性判定
「找 island」就是找 connected components。外層掃描未拜訪的合法節點，一次 BFS 走完一個 component；若還要判斷面積、是否碰邊界等屬性，就在遍歷時累積，最後再決定是否計入答案。屬性已經判定不合格，也不代表可以提前停止遍歷，因為仍需把整個 component 標記完。

把 queue 的入口條件固定成「合法且未看過的節點」，入隊時立即標記，出隊時就能專心處理節點與探索鄰居。起點也必須遵守同一條規則。若允許修改 grid，可用原地值取代 visited；這省掉 visited 陣列，但 queue 的空間仍須計入。

## Template Code
```cpp
queue<Node*> q;
unordered_set<Node*> visited;
q.push(start);
visited.insert(start);

while (!q.empty()) {
    Node* cur = q.front();
    q.pop();

    for (Node* next : cur->neighbors) {
        if (visited.contains(next)) {
            continue;
        }
        visited.insert(next);
        q.push(next);
    }
}
```

## Pitfalls
- 新節點第一次被 discover 時，要把「mark / create → enqueue → 之後 process」整條 transition 做完整；只 create 不 enqueue 會讓 traversal 停在第一層。
- visited 應該在 enqueue 時標記，而不是 dequeue 才標，避免同一節點重複進 queue。
- Graph 有 cycle；clone 類問題可直接用 `original -> copy` mapping 取代額外的 visited set。
- `unordered_map` 的 lookup / insert 平均 O(1)；若改用 `map`，整體會多出 `log V` 因子。

---

## Problems

### [[133] Clone Graph](../../problems/bfs/clone_graph.md)
**Complexity:** Time O(V + E), Space O(V)
- **Trigger:** Connected graph deep copy；每個 original node 都要對應唯一 clone，且 neighbors 關係必須保留
- **Insight:** 用 `unordered_map<Node*, Node*>` 同時保存 original → clone mapping 與 visited；第一次看到 neighbor 時 create + enqueue，每次看到 edge 都把對應 clone 接上
- **Pitfall:** 第一次 discover neighbor 時若只 create clone、忘了 `q.push(neighbor)`，BFS 只會處理起點那一層

### [[1254] Number of Closed Islands](../../problems/bfs/number_of_closed_islands.md)
**Complexity:** Time O(mn), Space O(mn)
- **Trigger:** 找出 grid 中由 `0` 組成、且被 `1` 包圍的 connected components
- **Insight:** 一次 BFS 走完整個 component，記錄是否碰到網格邊界；只有 `0`、`1` 時，不碰邊界就代表封閉
- **Pitfall:** 起點與鄰居都要在入隊時標記；碰到邊界也要繼續走完，邊界索引是 `m - 1`、`n - 1`
