# BFS — State-space BFS

## When to Use
- 題目要求最短步數，而且每一步成本相同，但「目前位置」不足以完整描述未來能做的選擇。
- 同一個座標可能因為剩餘資源、持有物品或已完成條件不同，而代表不同狀態。
- 常見額外狀態：剩餘消除次數、鑰匙 bitmask、已訪問集合 bitmask、剩餘燃料、是否使用過特殊能力。

核心判斷：**如果兩次到達同一個位置，未來可走的路不一定一樣，就不能只用位置當 visited key。** 要把所有會影響未來 transition 的資訊一起放進 state。

## Template Code
```cpp
queue<State> q;
q.push(start);
markVisited(start);

while (!q.empty()) {
    State cur = q.front();
    q.pop();

    if (isGoal(cur)) return distance(cur);

    for (State nxt : transitions(cur)) {
        if (!isValid(nxt)) continue;
        if (isVisited(nxt)) continue;
        markVisited(nxt);
        q.push(nxt);
    }
}
return -1;
```

## State 是搜尋圖上的節點，不只是座標
原本的 grid 可以把每個 `(x, y)` 看成一個 node；加入額外資源後，同一個座標會被拆成多個 node。例如有一次破牆能力時：

- `(x, y, unused)`
- `(x, y, used)`

兩者位置相同，但未來可走的 edge 不同，因此不能合併 visited。更一般地，若有 `k + 1` 種剩餘資源值，最多就有 `m·n·(k+1)` 個 state。

## 為什麼 BFS 第一次到終點就是最短
BFS 按步數由小到大展開 state。只要每個 transition 的成本都相同，queue 中所有距離 `d` 的 state 都會在距離 `d+1` 的 state 之前被處理，因此第一次 dequeue 到目標 state 時，它的距離就是全域最短。

這個保證建立在「visited 的單位是完整 state」上。若錯把 `(x, y, remaining)` 壓成只有 `(x, y)`，可能先用較差的資源狀態抵達某格，反而把之後更有能力的狀態擋掉。

## Dominance Pruning
有些題目可以把多維 visited 再壓縮：如果兩個 state 在同一位置，距離不更短且資源還更少，這個 state 被另一個 state 完全支配，可以丟掉。

例如破牆題中，若 BFS 已在 `(x, y)` 看過 `remaining = 5`，之後同樣或更晚才到達 `(x, y, remaining = 3)`，後者沒有任何優勢，可以 prune。這類優化要先證明「更多資源永遠不會讓未來選擇變差」，不能看到多維 state 就一律壓成 2D。

## Pitfalls
- **visited 少一個維度**：`visited[x][y]` 會把未來能力不同的 state 錯誤合併。
- **先檢查舊 state、再做 transition**：應該先根據下一格算出完整的 `nextState`，再檢查 `visited[nextState]`。
- **DFS + visited 直接拿來求最短路**：DFS 第一次到某 state 不保證是最短距離；若硬用 DFS，還要額外維護距離 relaxation 與 cycle 管理。等權最短路優先想到 BFS。
- **忘記初始化起點距離 / visited**：起點通常要先標成距離 0，否則鄰居距離會從錯誤的 sentinel 值推導。
- **把 queue 內的額外 state 當成冗餘**：只有「不影響未來 transition」的資訊才可省略；會改變可走路徑的資源一定要留。

---

## Problems

### [[1293] Shortest Path in a Grid with Obstacles Elimination](../../problems/bfs/shortest_path_in_a_grid_with_obstacles_elimination.md)
**Complexity:** Time O(m·n·k), Space O(m·n·k)
- **Trigger:** 最短路 + 最多可消除 `k` 個障礙；同一格因剩餘消除次數不同而有不同未來選擇
- **Insight:** BFS state 擴成 `(x, y, remaining)`，visited / dist 也必須以完整 state 為 key
- **Pitfall:** 不要在算出 `nr = remaining - grid[nx][ny]` 前就用舊的 remaining 檢查 visited
