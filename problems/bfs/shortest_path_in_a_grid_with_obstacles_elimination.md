# [1293] Shortest Path in a Grid with Obstacles Elimination
**Pattern:** [BFS → State-space BFS](../../patterns/bfs/state-space-bfs.md)
**Complexity:** Time O(m·n·k), Space O(m·n·k)
**Link:** https://leetcode.com/problems/shortest-path-in-a-grid-with-obstacles-elimination/

## Trigger Signals
- 求 grid 上的 **minimum steps**，而且上下左右每一步成本都相同 → 先想到 BFS。
- 題目多給一個「最多可消除 `k` 個障礙」的資源限制；到達同一個 `(x, y)` 時，剩餘消除次數不同會改變之後能走的路。
- 因此 `(x, y)` 不足以代表搜尋狀態，visited / distance 必須把 remaining 一起納入。

## Core Insight
把原本每個 grid cell 的單一節點拆成多個 state：`(x, y, remaining)`。走到 `0` 時 remaining 不變；走到 `1` 時 remaining 減 1，若變成負數就不能走。

BFS 按步數由小到大擴張完整 state，所以第一次 dequeue 到 `(m-1, n-1, any_remaining)` 時，就已經是全域最短路徑，可以直接 return。

## Why It's Correct
### 為什麼同一座標必須保留不同 remaining
`(x, y, 3)` 和 `(x, y, 0)` 雖然位置相同，但前者之後還能穿過最多 3 個障礙，後者完全不能。兩者的 outgoing transitions 不同，因此在搜尋圖上本來就是不同節點；若只用 `visited[x][y]`，可能先用掉資源的較差狀態把之後仍保有資源的狀態錯誤擋掉。

### 為什麼第一次到終點就是最短
把每個 `(x, y, remaining)` 視為一個 graph node，每次上下左右移動都是 cost 1 的 edge。本題因此是一張 unweighted state graph。BFS 會先處理距離 `d` 的所有 state，再處理距離 `d+1`，所以某個 state 第一次被訪問時就是它的最短距離；同理，第一次 dequeue 到任一終點 state 時就是整體最短答案。

## Complexity Analysis
- **Time O(m·n·k)**：最多有 `m·n·(k+1)` 個不同 state；每個 state 最多入 queue 一次，每次只檢查 4 個方向，所以總工作量是 O(m·n·k)。
- **Space O(m·n·k)**：`dist[x][y][remaining]` 共有 `m·n·(k+1)` 格，queue 最壞也可能持有同階的大量 state，因此同階為 O(m·n·k)。

## Solution Code
```cpp
class Solution {
public:
    int shortestPath(vector<vector<int>>& grid, int k) {
        int m = grid.size();
        int n = grid[0].size();
        vector<vector<vector<int>>> dist(
            m, vector<vector<int>>(n, vector<int>(k + 1, -1)));
        queue<tuple<int, int, int>> q;
        q.push({0, 0, k});
        dist[0][0][k] = 0;
        while (q.size()) {
            auto [x, y, r] = q.front();
            q.pop();
            if (x == m - 1 && y == n - 1) {
                return dist[x][y][r];
            }
            for (int i = 0; i < 4; i++) {
                int nx = x + dirs[i];
                int ny = y + dirs[i + 1];

                if (nx < 0 || nx >= m || ny < 0 || ny >= n) {
                    continue;
                }
                int nr = r - grid[nx][ny];

                if (nr < 0) {
                    continue;
                }
                if (dist[nx][ny][nr] != -1) {
                    continue;
                }
                dist[nx][ny][nr] = dist[x][y][r] + 1;
                q.push({nx, ny, nr});
            }
        }
        return -1;
    }

private:
    int dirs[5] = {-1, 0, 1, 0, -1};
};
```

## Alternatives / Optimization
### Dominance pruning：每格只記目前看過的最大 remaining
同一個位置若已用更短或相同距離到達，且剩餘資源更多，較少 remaining 的 state 沒有任何未來優勢，可以 prune。可把 3D `dist` 改成 2D `bestRemaining[x][y]`，只有新的 `remaining` 大於紀錄時才繼續入隊。

這個優化把 visited / dominance table 從 O(m·n·k) 降成 O(m·n)；每格的 best remaining 最多改善 `k+1` 次，因此最壞時間仍可到 O(m·n·k)。在固定 4 鄰居的 grid 上，queue frontier 也可維持在 O(m·n) 級別。

### `k` 足夠大時直接走 Manhattan shortest path
任一只向右 / 向下的 Manhattan shortest path 長度都是 `m+n-2`，途中最多有 `m+n-3` 個可成為障礙的中間格。如果 `k >= m+n-3`，一定能挑一條最短幾何路徑一路消掉遇到的障礙，答案可直接回傳 `m+n-2`。

## Pitfalls
- **visited 只開 2D**：`(x, y, remaining)` 才是完整 state；remaining 不同時未來能力不同，不能合併。
- **用舊的 `r` 先檢查 visited**：下一格如果是障礙，真正要訪問的是 `(nx, ny, r-1)`。應先算 `nr = r - grid[nx][ny]`，確認 `nr >= 0` 後，再檢查 `dist[nx][ny][nr]`。
- **忘記 `dist[0][0][k] = 0`**：若 sentinel 是 `-1`，第一層距離會從 `-1 + 1` 算成 0，整份答案少 1。
- **最後直接對所有 remaining 做 `min_element`**：未到達的 state 是 `-1`，會把真正距離蓋掉。BFS 更乾淨的寫法是第一次 dequeue 到終點就直接 return。
- **DFS 也能枚舉，但不天然保證最短**：DFS 需要 cycle 管理，還要額外維護距離 / relaxation；BFS 也要避免重複 state，但在等權圖上第一次訪問完整 state 就已是最短，因此單純 visited 即可。

## Side Notes
### BFS 與 DFS 的 cycle / shortest-path 差別
兩者都需要處理 cycle。差別不是「BFS 不需要 visited」，而是等權圖中 BFS 的 traversal order 本身就是距離順序，所以完整 state 第一次被訪問即可定案；DFS 第一次抵達可能走了繞路，不能因為 visited 就永久擋住之後更短的到達方式。

### `tuple` 的 structured binding
Queue state 用 `tuple<int, int, int>` 時，可以直接寫 `auto [x, y, r] = q.front();`，比反覆 `get<0>()`、`get<1>()`、`get<2>()` 更容易讀。

## Related Problems
- [286] Islands and Treasure (Walls and Gates) — [同一個 BFS 基礎](islands_and_treasure.md)，但 state 只有座標；1293 正好展示「座標不足時要擴 state」
- [1091] Shortest Path in Binary Matrix — 單純 grid BFS，沒有額外資源 state，適合對照普通 2D visited
- [864] Shortest Path to Get All Keys — state 擴成 `(x, y, keyMask)`；bitmask 代表目前持有的鑰匙
- [847] Shortest Path Visiting All Nodes — state 擴成 `(node, visitedMask)`；位置相同但走過的節點集合不同就是不同 state
