# BFS — Graph Traversal

## When to Use
- 題目不是要最短路，而是要從一個起點把整個 connected component 都走完。
- 常見需求：複製 graph、收集所有 reachable nodes、沿 adjacency list 傳播資訊。
- 若 graph 保證 connected，從任一給定起點跑一次 BFS 就能遍歷所有節點；若不保證 connected，還需要從未訪問節點重新啟動 traversal。

這類題的核心不是 level，而是「每個節點只處理一次，所有 edge 都掃到」。對 clone 類問題，可以把 `original -> copy` mapping 同時當成 visited。

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
