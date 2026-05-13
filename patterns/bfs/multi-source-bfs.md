# BFS — Multi-source BFS

## When to Use
- Grid 或圖上有**多個**「答案來源」，要對**每個**查詢點問「離最近的來源多遠 / 能不能被來源觸及」
- 答案具有**單調擴散性**：來源 A → 中繼 B → 目標 C 成立，且每一步成本相同
- 題目敘述：腐爛、火災、感染、信號、淹水、最近的 X、能否被某類東西到達

**辨認訊號**：「每個格子都要問同一件事」+「答案的『來源』數量比查詢點少」→ 反過來從來源出發廣播。

與單源 BFS 的差別：把所有來源**同時**塞進 initial queue（全部視為 level 0），之後流程一模一樣。BFS 的「第一次碰到就是最短」性質會自動處理多源競爭——每格被距離它最近的那個來源先碰到。

## 為什麼這樣是對的
直覺：如果獨立對每個來源跑 BFS 再對每格取最小值，跟「多源一起擴散」結果相同；但後者把所有 BFS 合併成一次遍歷，每格只被 visit 一次。

形式化：把所有來源接到一個虛擬「超級源點」上、每條邊權 0，從超級源點跑單源 BFS — 跟多源 BFS 完全等價。

## Template Code
```cpp
queue<pair<int,int>> q;
for (int i = 0; i < m; i++)
    for (int j = 0; j < n; j++)
        if (isSource(grid[i][j])) {
            // source itself sits at distance 0 (or mark visited)
            q.push({i, j});
        }

constexpr int dirs[5] = {1, 0, -1, 0, 1};
while (!q.empty()) {
    auto [x, y] = q.front(); q.pop();
    for (int k = 0; k < 4; k++) {
        int nx = x + dirs[k], ny = y + dirs[k+1];
        if (nx < 0 || nx >= m || ny < 0 || ny >= n) continue;
        // walls and filled cells blocked
        if (!canFill(grid[nx][ny])) continue;
        // write distance; doubles as visited
        grid[nx][ny] = grid[x][y] + 1;
        q.push({nx, ny});
    }
}
```

關鍵技巧：
- **把距離寫回 grid 本身當作 visited 標記**，省一個獨立 `visited` array。前提是「未訪問」有個可辨識的哨兵值（INF、-1、特定字元）
- **不需要在 queue 裡存距離**：從 `grid[x][y]` 讀就好，`pair<int,int>` 比 `tuple<int,int,int>` 小、cache 更友善
- 若需要「層數」（如腐爛橘子要回傳最後一層的時間）才需要分層迴圈 `while (sz--)`

## Pitfalls
- **初始化時把所有來源一起 push**，不是邊 BFS 邊發現來源
- **push 時就標 visited / 寫距離**，不是 pop 時才標。否則同一格可能被多個鄰居重複入隊
- 終點 / 牆 / 未訪問三類值要區分清楚；用 `grid[nx][ny] != INF` 當 prune 條件時，要確保 `-1`（牆）不會被誤判為 visited
- 想要「每個來源的勢力範圍」之類的歸屬資訊就不適用單純模板，要額外記 `parent` 或 `owner`

---

## Problems

### [[286] Islands and Treasure (Walls and Gates)](../../problems/bfs/islands_and_treasure.md)
**Complexity:** Time O(m·n), Space O(m·n)
- **Trigger:** 每個 room 都要問「離最近 treasure 多遠」、treasure 數量 << room 數量
- **Insight:** 反向從所有 treasure 同步擴散，距離直接寫回 grid 兼當 visited
- **Pitfall:** push 時就要寫距離（=標記 visited），不是 pop 時；queue 不必存距離，從 grid 讀
